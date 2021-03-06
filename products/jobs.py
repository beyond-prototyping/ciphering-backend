# -*- coding: utf-8 -*-
from base64 import b64encode
import json
import os
import tempfile

import django_rq
import envoy
import requests
from django.conf import settings
from django.core.mail import send_mail
from requests_oauthlib import OAuth1
from .models import Order
from .utils import s3bucket


def fetch_job(job_id):
    queue = django_rq.get_queue()
    try:
        job = queue.fetch_job(job_id)
    except:
        job = queue.safe_fetch_job(job_id)
    return job


def fetch_order(order_id):
    order = Order.objects.get(id=order_id)
    return order


def compile_scad_to_stl(order_id):
    order = fetch_order(order_id)

    order.status = Order.STATUS_COMPILING
    order.save()
    bucket = s3bucket()
    key = bucket.get_key('scad:{0}'.format(order.uuid))

    scad_file = tempfile.mktemp('.scad')
    with open(scad_file, 'w') as f:
        f.write(key.get_contents_as_string())

    stl_file = tempfile.mktemp('.stl')

    try:
        r = envoy.run('{binary} -o {stl_file} {scad_file}'.format(
            binary=settings.OPENSCAD_BINARY,
            stl_file=stl_file,
            scad_file=scad_file
        ))
    except:
        raise Exception("Conversion failed, executable not found?")
    finally:
        os.unlink(scad_file)

    if r.status_code == 0:
        bucket = s3bucket()
        key = bucket.new_key('stl:{0}'.format(order.uuid))
        key.set_contents_from_filename(stl_file)

        order.status = Order.STATUS_COMPILED
        order.save()
        return key.key
    else:
        print settings.OPENSCAD_BINARY, scad_file, stl_file, r.std_out, r.std_err
        order.status = Order.STATUS_FAILED
        order.save()
        raise Exception("Conversion failed with error {0}".format(r.status_code))


def upload_stl_to_shapeways(compile_job_id, order_id, materials, default_material, title):
    job = fetch_job(compile_job_id)
    order = fetch_order(order_id)

    bucket = s3bucket()
    key = bucket.get_key(job.result)
    stl = key.get_contents_as_string()

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

    model_data = r.json()

    order.status = Order.STATUS_UPLOADED
    order.shapeways_url = model_data['urls']['publicProductUrl']['address']
    order.save()

    return model_data


def send_email(upload_job_id, order_id, email):
    job = fetch_job(upload_job_id)
    order = fetch_order(order_id)

    r = send_mail('Your CipheRing is now ready to order!', 'Woohoo! Your CipheRing is now ready to order at this URL: {0}'.format('{0}/order/?id={1}&from=email'.format(settings.FRONTEND_BASE_URL, order.uuid)), 'CipheRing <admin+ciphering@pb.io>', [email], fail_silently=False)

    order.status = Order.STATUS_NOTIFIED
    order.save()

    return r
