from base64 import b64encode
import json
import os.path
import re
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
import requests
from requests_oauthlib import OAuth1, OAuth1Session
from cStringIO import StringIO
from urlparse import parse_qs


def authenticate_with_shapeways(request):
    if request.GET.has_key('oauth_token') and request.GET.has_key('oauth_verifier'):
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
            print credentials
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
        parameters.append('{0} = {1};'.format(key, params[key]))

    scad = source_file.read()
    regex = re.compile(r'// PARAMETERS:START //(.*)// PARAMETERS:END //', re.DOTALL)
    scad = re.sub(regex, "\n".join(parameters), scad)

    return scad


def convert_scad_to_stl(scad):
    r = requests.post(settings.SCAD2STL_URL, files={'file': ('ciphering.scad', StringIO(scad))})
    return r.content


def upload_stl(stl, materials, default_material, title):
    oauth = OAuth1(
        client_key=settings.SHAPEWAYS_CONSUMER_KEY,
        client_secret=settings.SHAPEWAYS_CONSUMER_SECRET,
        resource_owner_key=settings.SHAPEWAYS_RESOURCE_OWNER_KEY,
        resource_owner_secret=settings.SHAPEWAYS_RESOURCE_OWNER_SECRET,
    )

    data = dict(
        file=b64encode(stl),
        fileName='ciphering.stl',
        hasRightsToModel=1,
        acceptTermsAndConditions=1,
        title=title,
        uploadScale=0.001,
        defaultMaterialId=default_material,
        materials=materials,
        isForSale=1
    )

    r = requests.post(url='https://api.shapeways.com/models/v1', data=json.dumps(data), auth=oauth)
    return r.json()


def create_product(request):
    source_file = open(os.path.join(settings.BASE_DIR, 'scad', 'CipheRing.scad'))
    params = json.loads(request.GET.get('param'))
    scad = compile_scad(source_file, params)
    # stl = convert_scad_to_stl(scad)
    stl = open(os.path.join(settings.BASE_DIR, 'scad', 'ciphering.stl')).read()

    materials = {}
    for material_id in settings.SHAPEWAYS_MATERIALS:
        materials[material_id] = dict(
            materialId=material_id,
            isActive=1
        )

    model_data = upload_stl(stl=stl, materials=materials, default_material=params['material'], title='CipheRing [{0}]'.format(params['digits']))
    return HttpResponseRedirect('https://www.shapeways.com/model/{0}/?key={1}'.format(model_data['modelId'], model_data['secretKey']))
