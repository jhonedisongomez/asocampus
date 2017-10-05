
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
        'NAME': 'db3bjjs55629je',
        'USER': 'hgmldlkwqtoytl',
        'PASSWORD': '1ee8f590d525c6957355fa6e21741f467f05fca8aa2627d33132f0e9b378118b',
        'HOST': 'ec2-23-21-220-188.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

