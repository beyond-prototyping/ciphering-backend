import json
import math
import os.path
import re
import tempfile
from urlparse import parse_qs

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.utils import six
from django.views.decorators.csrf import csrf_exempt
import django_rq
import requests
from requests_oauthlib import OAuth1

from .jobs import compile_scad_to_stl, upload_stl_to_shapeways, send_email
from .models import Order
from .utils import create_pattern


def authenticate_with_shapeways(request):
    if 'oauth_token' in request.GET and 'oauth_verifier' in request.GET:
        access_token_url = 'https://api.shapeways.com/oauth1/access_token/v1'
        oauth = OAuth1(
            client_key=settings.SHAPEWAYS_CONSUMER_KEY,
            client_secret=settings.SHAPEWAYS_CONSUMER_SECRET,
            resource_owner_key=request.GET['oauth_token'],
            resource_owner_secret=request.session['credentials']['oauth_token_secret'][0],
            verifier=request.GET['oauth_verifier']
        )
        r = requests.post(url=access_token_url, auth=oauth)
        if r.ok:
            credentials = parse_qs(r.content)
            request.session['credentials'] = credentials
            return_url = request.session.get('return_url')
            if return_url is not None:
                return HttpResponseRedirect(return_url)
            else:
                return HttpResponse('Authenticated successfully.')
        else:
            try:
                error_msg = json.loads(r.content)['reason']
            except:
                error_msg = 'Something went wrong'
            return HttpResponseServerError(u'<h1>{0}</h1><a href="./">Try again</a>'.format(error_msg))
    else:
        request_token_url = 'https://api.shapeways.com/oauth1/request_token/v1'
        oauth = OAuth1(
            client_key=settings.SHAPEWAYS_CONSUMER_KEY,
            client_secret=settings.SHAPEWAYS_CONSUMER_SECRET,
            callback_uri='http://localhost:5000/authenticate/'
        )
        r = requests.post(url=request_token_url, auth=oauth)
        request.session['credentials'] = parse_qs(r.content)
        request.session['return_url'] = request.GET.get('return_url')
        return HttpResponseRedirect(request.session['credentials']['authentication_url'][0])


def compile_scad(source_file, params):
    parameters = []

    for key in params:
        if isinstance(params[key], six.string_types):
            value = '"{0}"'.format(params[key])  # TODO: replace '"' in value
        else:
            value = params[key]
        parameters.append('{0} = {1};'.format(key, value))

    scad = source_file.read()
    regex = re.compile(r'// PARAMETERS:START //(.*)// PARAMETERS:END //', re.DOTALL)
    scad = re.sub(regex, "\n".join(parameters), scad)
    scad = re.sub('use <([^>]+)>', lambda m: open(os.path.join(settings.BASE_DIR, 'scad', m.group(1))).read(), scad)
    scad = re.sub('font = "([^"]+)"', lambda m: 'font = "{0}"'.format(os.path.join(settings.BASE_DIR, 'scad', m.group(1))), scad)

    return scad


@csrf_exempt
def create_product(request):
    params = {
        'ringRadius': float(request.POST.get('ringsize')) / (math.pi * 2),
        'initials1': request.POST.get('initials1'),
        'initials2': request.POST.get('initials2'),
        'pattern': create_pattern(request.POST.get('digits'))
    }

    order = Order.objects.create(
        params=params,
        digits=request.POST.get('digits', ''),
        material=request.POST.get('material', 0),
        email=request.POST.get('email', ''),
    )

    source_file = open(os.path.join(settings.BASE_DIR, 'scad', 'CipheRing.scad'))
    scad = compile_scad(source_file, params)

    scad_file = tempfile.mktemp('.scad')
    f = open(scad_file, 'w')
    f.write(scad)
    f.close()

    materials = {}
    for material_id in settings.SHAPEWAYS_MATERIALS:
        materials[material_id] = dict(
            materialId=material_id,
            isActive=1,
            markup=float(settings.SHAPEWAYS_MARKUP),
        )

    compile_job = django_rq.enqueue(compile_scad_to_stl, kwargs={
        'order_id': order.id,
        'scad_file': scad_file,
    })

    upload_job = django_rq.enqueue(upload_stl_to_shapeways, kwargs={
        'compile_job_id': compile_job.id,
        'order_id': order.id,
        'materials': materials,
        'default_material': order.material,
        'title': 'CipheRing[{0}{1}{2}]'.format(request.POST.get('digits'), params['initials1'], params['initials2']),
    }, depends_on=compile_job)

    email_job = django_rq.enqueue(send_email, kwargs={
        'upload_job_id': upload_job.id,
        'order_id': order.id,
        'email': request.POST.get('email') or settings.ADMINS[0][1],
    }, depends_on=upload_job)

    order.compile_job_id = compile_job.id
    order.upload_job_id = upload_job.id
    order.email_job_id = email_job.id
    order.save()

    return HttpResponseRedirect('{0}/order/?id={1}'.format(settings.FRONTEND_BASE_URL, order.uuid))


def order_status(request, order_uuid):
    try:
        order = Order.objects.get(uuid=order_uuid)
    except Order.DoesNotExist:
        return HttpResponse('{"status": "not-found"}', content_type='application/json')

    return HttpResponse(json.dumps(dict(
        status=order.status,
        description=order.get_status_display(),
        shapeways_url=order.shapeways_url,
    )), content_type='application/json')
