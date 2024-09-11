"""
Django settings for testBranch project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
devMode = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'dhsclubs.org@gmail.com'

if not devMode:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = os.getenv('SECRET_KEY')

    # SECURITY WARNING: don't run with debug turned on in production!
    # will not serve static files automatically without debug
    if os.getenv('DEBUG') == "false":
        DEBUG = False
    else:
        DEBUG = True
    
    # posting will fail without PASSWORD
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASS') # ONLY PERSON HOSTING SHOULD KNOW PASSWORD
else:
    DEBUG = True
    SECRET_KEY = "development-key-exposedEUkm398278sunL98e89"
    EMAIL_HOST_PASSWORD = "notThePassword"

ALLOWED_HOSTS = ["https://dhsclubs.org", "https://www.dhsclubs.org", "http://127.0.0.1", "http://dhsclubs.org", "http://www.dhsclubs.org", "*"]
CSRF_TRUSTED_ORIGINS = ["https://dhsclubs.org", "https://www.dhsclubs.org", "http://127.0.0.1", "http://dhsclubs.org", "http://www.dhsclubs.org"]

ADMINS = [("Cody", "zcody007@gmail.com")]

# Application definition
SITE_ID = 4

# most secure way is to set to false rather than true. POST requests are much more secure.
# Not high priority because we don't store sensitive data
SOCIALACCOUNT_LOGIN_ON_GET = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'users',
]

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email"
        ],
        "AUTH_PARAMS": {"access_type": "online", 
                        "include_granted_scopes": "false",
                        },
        "VERIFIED_EMAIL": True,
        'OAUTH2_PARAMS': {
            'redirect_uri': 'http://django.com/accounts/google/login/callback/',
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'testBranch.urls'

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

WSGI_APPLICATION = 'testBranch.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
if devMode:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'prod.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

#STATIC_URL = '/home/cody/Documents/DjangoProjects/OCRWebsite-1/helloWorld/testBranch/static/' # FOR SERVER

STATIC_URL = '/static/' # FOR LOCALS
STATIC_ROOT = '/static/'

#STATIC_ROOT=os.path.join(BASE_DIR, "static") #???

STATICFILES_DIRS = (os.path.join(BASE_DIR, "assests"),)

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

#SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

#ACCOUNT_ADAPTER = 'users.adapters.MyAccountAdapter'
#SOCIALACCOUNT_ADAPTER = 'users.adapters.MySocialAccountAdapter'

#ACCOUNT_ADAPTER = 'users.authConfig.MyAccountAdapter'
LOGIN_REDIRECT_URL = "/clubs/"
LOGOUT_REDIRECT_URL = "/"