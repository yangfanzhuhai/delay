"""
Django settings for delaysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd!)ix534sv&ew+0t6+3m6z05z9+l(80=!4%c#zl98*u2b&eu-j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'delay'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'delaysite.urls'

WSGI_APPLICATION = 'delaysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# DATABASES = {
#     'default': {
#         'NAME': 'tfl_bus', 
#         'ENGINE': 'sql_server.pyodbc',
#         'HOST': 'sqlserver.doc.ic.ac.uk',
#         'USER': 'yz10111',
#         'PASSWORD': 'TFL2dbSS',
#         'PORT': 1433,
#         'OPTIONS': {
#             'driver': 'FreeTDS',
#             # 'dsn': 'sqlserver.doc.ic.ac.uk',
#             'host_is_server': True,
#             'extra_params': "TDS_VERSION=8.0"
#         }
#     }
# }

# DATABASES = {
#     'default': {
#         'NAME': 'delay', 
#         'ENGINE': 'django.db.backends.mysql',
#         'HOST': 'delay.doc.ic.ac.uk',
#         'USER': 'delay',
#         'PASSWORD': 'CcwLCw3Kcs9Py33T',
#         'PORT': 3306
#     }
# }

DATABASES = {
    'default': {
        'NAME': 'yz10111', 
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'db.doc.ic.ac.uk',
        'PORT': 5432,
        'USER': 'yz10111',
        'PASSWORD': 'pGmhDilp2v'
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'GB'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
