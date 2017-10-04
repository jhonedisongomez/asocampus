
from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['*']
# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd94nj8jspsvrrr',
        'USER': 'ryatnbyeiiispb',
        'PASSWORD': '1ef2eff4838a5150c56057ed585334dbd478f0ceae3b2a98ec2915720141609b',
        'HOST': 'ec2-50-17-203-195.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

