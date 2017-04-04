
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
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': '192.168.1.58',
        'PORT': '5432',
    }
}
# Static files (CSS, JavaScript, Images)
