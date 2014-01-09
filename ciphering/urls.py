import json
import math
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.template import Template
from django.views.generic import View
from django.contrib import admin
from django.contrib.auth.models import User, Group
import requests
from requests_oauthlib import OAuth1, OAuth1Session
from rest_framework import viewsets, routers
from rest_framework.views import APIView
from rest_framework.response import Response


router = routers.DefaultRouter()

class ListMaterials(APIView):
    def get(self, request, format=None):
        oauth = OAuth1(
            client_key=settings.SHAPEWAYS_CONSUMER_KEY,
            client_secret=settings.SHAPEWAYS_CONSUMER_SECRET,
            resource_owner_key=settings.SHAPEWAYS_GENERIC_OAUTH_TOKEN,
            resource_owner_secret=settings.SHAPEWAYS_GENERIC_OAUTH_TOKEN_SECRET
        )
        r = requests.get(url='https://api.shapeways.com/materials/v1', auth=oauth)
        data = json.loads(r.content)
        materials = []
        supported_material_ids = settings.SHAPEWAYS_MATERIALS
        for id in supported_material_ids:
            materials.append([data['materials'][material_id] for material_id in data['materials'] if int(material_id) == id][0])
        return Response(materials)


class ListRingsizes(APIView):
    def get(self, request, format=None):
        data = [{'circumference': c, 'diameter': round(c/math.pi, 1)} for c in range(40,70)]
        return Response(data)


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^authenticate/$', authenticate_with_shapeways),
    url(r'^materials/$', ListMaterials.as_view()),
    url(r'^ringsizes/$', ListRingsizes.as_view()),
    url(r'^products/create/$', 'products.views.create_product'),
    # url(r'^compile-scad/$', compile_scad),
    # url(r'^upload/$', upload_stl),
)
