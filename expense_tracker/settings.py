"""
Django settings for expense_tracker project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY',
                            'TheActualNewLord@21goingto22nextyear')
# SECRET_KEY = "THEBOYAMMIEL21"

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get('DEBUG'):
    DEBUG = eval(os.environ.get('DEBUG'))
else:
    DEBUG = False
# DEBUG = True

if DEBUG:
    ALLOWED_HOSTS = ['finsense.herokuapp.com', '127.0.0.1']
else:
    ALLOWED_HOSTS = ['finsense.herokuapp.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'activity.apps.ActivityConfig',
    'users.apps.UsersConfig',

    'crispy_forms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'expense_tracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'money': 'activity.templatetags.money',
            },
        },
    },
]

WSGI_APPLICATION = 'expense_tracker.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DB_NAME = os.environ.get("DATABASE_NAME")
USER = os.environ.get("DATABASE_USER")
HOST = os.environ.get("DATABASE_HOST")
ENGINE = 'django.db.backends.postgresql'
PASSWORD = os.environ.get('DATABASE_PASSWORD')
os.environ.get('')

if DEBUG:
    DB_NAME = BASE_DIR / "db.sqlite3"


DATABASES = {
    'default': {
        'ENGINE': ENGINE,
        'NAME': DB_NAME,
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': HOST,
        'PORT': '5432'
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# STATIC_ROOT = STATIC_DIR

if not DEBUG:
    STATIC_ROOT = STATIC_DIR
else:
    STATICFILES_DIRS = [STATIC_DIR,]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'activity:home'
LOGOUT_REDIRECT_URL = 'activity:index'
