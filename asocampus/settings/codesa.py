
from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['*']
# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'asocampus',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '10.11.6.6',
        'PORT': '5432',
    }
}

