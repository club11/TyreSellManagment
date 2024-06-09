"""
Django settings for proj project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from tokenize import Ignore

import os

from celery.schedules import crontab

#from ignore_data import KEY
#from . secret_key import SECRET_KEY

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY='django-insecure-(@71mq+18c)co_!&tmw_f8fr*hpf9-@2tjq!rmmdt1-b9v+!l6',
#SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.0.136',]
#ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tyres',
    #'googlecharts',
    'dictionaries',
    'filemanagment',
    'abc_table_xyz',   
    'sales', 
    'homepage',
    'prices',
    'chemcurier',
    'profiles',

#    'crispy_forms',
    'django.contrib.postgres', #это модуль Django, который предоставляет интеграцию с базой данных PostgreSQL
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'proj.urls'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
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

WSGI_APPLICATION = 'proj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

###### ПЕРЕД сборкой докер-контейнера раскоментить sqlite3 и закоментить postgresql:
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }   
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres_db',
        'USER': 'postgres_db',
        'PASSWORD': 'postgres_db',
        'HOST': '127.0.0.1',
        'PORT': '5433',
    }
}
##### END ПЕРЕД сборкой докер-контейнера раскоментить sqlite3 и закоментить postgresql

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
EMAIL_HOST_USER = 'club11@bk.ru'
EMAIL_HOST_PASSWORD = 'bh235zkBi7PKzaC0qVpr'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


###### ДЛЯ redis -celery
# 1/ для docker-compose:
#CELERY_BROKER_URL = "redis://redis:6379/0"
#CELERY_RESULT_BACKEND = "redis://redis:6379/0"
# 2/ для локальной машины:
#- ????
# 2/ для Synology:
CELERY_BROKER_URL = 'redis://192.168.0.136:6379/0'
# end

CELERY_BEAT_SCHEDULE = {
    'parcing': {
        'task': 'prices.views.running_programm',
        'schedule': crontab(hour=20, minute=4),
    },
    #'dfgdg': {
    #    'task': 'prices.views.dfgdg',
    #    'schedule': 5 #* 60,
    #},
}
###### END ДЛЯ redis -celery

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

#STATIC_ROOT = '/var/www/static/' - версия для pythonanywhere
##### ПЕРЕД сборкой докер-контейнера раскоментить

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
##### END ПЕРЕД сборкой докер-контейнера раскоментить

# для DEV:
MEDIA_URL = '/media/'  
MEDIA_ROOT = BASE_DIR /'media/'

######STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL)
######MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL) 

#STATICFILES_DIRS = [
#    BASE_DIR / "static",
#]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
LOGIN_REDIRECT_URL = '/chemcurier/chemcurier_progressive'