from os import environ as env
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '../.env')

SECRET_KEY = env.get('SECRET_KEY')
DEBUG = env.get('DEBUG', '').lower() == 'true'
ALLOWED_HOSTS = env.get('ALLOWED_HOSTS', '').split()

INSTALLED_APPS = [
    # Default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Outside apps
    'taggit',
    'rest_framework',
    'drf_spectacular',
    # Project apps
    'accounts',
]

MIDDLEWARE = [
    # Default middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Outside middleware
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'zoo_store.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'zoo_store.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / '../db.sqlite3',
    }
}


# Password validation

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'


# Media files

MEDIA_URL = 'media/'
MEDIA_ROOT = 'media'


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    INTERNAL_IPS = ['127.0.0.1']
