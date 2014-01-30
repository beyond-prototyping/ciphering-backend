"""
Django settings for ciphering project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

env = os.environ
truish_env = lambda v: os.environ.get(v, False) == 'True'

PROJECT_NAME = 'ciphering'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qg&w%3j&2hre$ih30=$bi9%^zpef_6tk@c8528ors$876xi(ff'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = truish_env('DEBUG')

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

ADMINS = (
    ('Philipp Bosch', 'hello+ciphering@pb.io'),
)


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'rest_framework',
    'werkzeug_debugger_runserver',
    'corsheaders',
    'django_rq',
    'products',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

ROOT_URLCONF = 'ciphering.urls'

WSGI_APPLICATION = 'ciphering.wsgi.application'

TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'emeisdeubel', 'templates'),
]


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {'default': dj_database_url.config()}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Cache

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': PROJECT_NAME
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = env.get('STATIC_URL', '/static/')
STATIC_ROOT = env.get('STATIC_ROOT')
MEDIA_URL = env.get('MEDIA_URL', '/media/')
MEDIA_ROOT = env.get('MEDIA_ROOT')



REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    # 'DEFAULT_MODEL_SERIALIZER_CLASS':
    #     'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ]
}

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.getenv('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = os.getenv('SENDGRID_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SHAPEWAYS_CONSUMER_KEY = env.get('SHAPEWAYS_CONSUMER_KEY')
SHAPEWAYS_CONSUMER_SECRET = env.get('SHAPEWAYS_CONSUMER_SECRET')
SHAPEWAYS_GENERIC_OAUTH_TOKEN = env.get('SHAPEWAYS_GENERIC_OAUTH_TOKEN')
SHAPEWAYS_GENERIC_OAUTH_TOKEN_SECRET = env.get('SHAPEWAYS_GENERIC_OAUTH_TOKEN_SECRET')
SHAPEWAYS_RESOURCE_OWNER_KEY = env.get('SHAPEWAYS_RESOURCE_OWNER_KEY')
SHAPEWAYS_RESOURCE_OWNER_SECRET = env.get('SHAPEWAYS_RESOURCE_OWNER_SECRET')
SHAPEWAYS_MATERIALS = [54,81,87,85,83]

SCAD2STL_URL = 'http://scad2stl.pbsit.es/'


CORS_ORIGIN_ALLOW_ALL = True


RQ_QUEUES = {
    'default': {
        'URL': os.getenv('REDIS_URL', 'redis://localhost:6379'),
        'DB': 0,
    },
}

OPENSCAD_BINARY = os.getenv('OPENSCAD_BINARY', '/opt/homebrew-cask/Caskroom/openscad/2013.06/OpenSCAD.app/Contents/MacOS/OpenSCAD')
FRONTEND_BASE_URL = os.getenv('FRONTEND_BASE_URL', 'http://localhost:4000')
