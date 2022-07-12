"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env_path = os.path.join(BASE_DIR, 'pharmacogenomics.env')
load_dotenv(env_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ugbnazv9chk*!1d2mfs(&w#beok=wqa%h_i8f&l_es=exl+u*n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# from django.conf import settings
# if not settings.configured:
#     settings.configure(myapp_defaults, DEBUG=True)

# Application definition

INSTALLED_APPS = [
    'pharmacogenomics.apps.PharmacogenomicsConfig',
    'pdbgen.apps.PdbgenConfig',
    'gtexome.apps.GtexomeConfig',
    'metabolites.apps.MetabolitesConfig',
    'precursors.apps.PrecursorsConfig',
    'precursor_metabolite_map.apps.PrecursorMetaboliteMapConfig',
    'drug_name_precursor_map.apps.DrugNamePrecursorMapConfig',
    'full_metabolite_map.apps.FullMetaboliteMapConfig',
    'api.apps.ApiConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_plotly_dash.middleware.BaseMiddleware',
    'django_plotly_dash.middleware.ExternalRedirectionMiddleware',#optional
]

X_FRAME_OPTIONS = 'SAMEORIGIN'

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
DCS_SESSION_COOKIE_SAMESITE = 'None'
DCS_SESSION_COOKIE_SAMESITE_FORCE_ALL = True

MIDDLEWARE_CLASSES = [
    'django_cookies_samesite.middleware.CookiesSameSite',
]

ROOT_URLCONF = 'pharmacogenomics_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'error.log',
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'info.log',
        }
    },
    'loggers': {
        'django.error': {
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.info': {
            'handlers': ['info'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

WSGI_APPLICATION = 'pharmacogenomics_website.wsgi.application'

BOOTSTRAP3 = {'include_jquery': True}


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

NAME = os.getenv('NAME')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': NAME,
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': HOST,
        'PORT': PORT,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)

STATICFILES_FINDERS = [

    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
    'django_plotly_dash.finders.DashAppDirectoryFinder',
]

PLOTLY_COMPONENTS = [

    # Common components (ie within dash itself) are automatically added
    # django-plotly-dash components
    'dpd_components',
    # static support if serving local assets
    # 'dpd_static_support',

    # Other components, as needed
    'dash_bootstrap_components',
]

STATIC_URL = '/static/'

PLOTLY_DASH = {

    # Route used for the message pipe websocket connection
    "ws_route" :   "dpd/ws/channel",

    # Route used for direct http insertion of pipe messages
    "http_route" : "dpd/views",

    # Flag controlling existince of http poke endpoint
    "http_poke_enabled" : True,

    # Insert data for the demo when migrating
    "insert_demo_migrations" : False,

    # Timeout for caching of initial arguments in seconds
    "cache_timeout_initial_arguments": 60,

    # Name of view wrapping function
    "view_decorator": None,

    # Flag to control location of initial argument storage
    "cache_arguments": True,

    # Flag controlling local serving of assets
    "serve_locally": False,
}