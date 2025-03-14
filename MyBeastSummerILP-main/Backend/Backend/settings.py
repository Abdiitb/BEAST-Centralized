"""
Django settings for Backend project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Read API Base URL from environment variable
# API_BASE_URL = os.getenv('REACT_APP_API_URL', 'http://localhost:8001')  # default to local in development
# CENTRAL_API_BASE = os.getenv('REACT_APP_CENTRALIZED_API_URL', 'http://localhost:8000')
API_BASE_URL = 'http://localhost:8001'
CENTRAL_API_BASE = 'http://localhost:8000'

# CENTRAL_API_BASE = 'http://centralized-backend-1:8000'
# API_BASE_URL = 'http://mybeastsummerilp-main-backend-1:8001'

# Load environment variables
ENV_MODE = os.getenv('ENV_MODE', 'dev')  # Default to 'dev' if ENV_MODE is not set
ENV_FILE = f"/app/.env.{ENV_MODE}"  # Docker mounts .env file here

if os.path.exists(ENV_FILE):
    load_dotenv(dotenv_path=ENV_FILE)

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")

# Debug Mode
# DEBUG = os.getenv("DEBUG", "False").lower() == "true"
DEBUG = True

# Allowed Hosts
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")


# Application definition

INSTALLED_APPS = [
    'import_export',
    'Blog',
    'Registrations',
    'rest_framework',
    "Authentication",
    'Backend',
    "Projects",
    'corsheaders',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Backend.urls"


CORS_ALLOW_ALL_ORIGINS = True


# CSRF_TRUSTED_ORIGINS = ['https://ilpsummer.sarc-iitb.org']

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",  
    "x-requested-with",
]


CORS_ALLOW_METHODS = [
    "DELETE",  
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "db.sqlite3",
    # }

    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': os.getenv("POSTGRES_DB"),
    #     'USER': os.getenv("POSTGRES_USER"),
    #     'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
    #     'HOST': os.getenv("DB_HOST"),
    #     'PORT': os.getenv("DB_PORT", 5432),
    # },

    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ilp',
        'USER': 'aryan',
        'PASSWORD': 'centralized',
        'HOST': 'localhost',
        'PORT': 5432,
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "django_static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# CSRF_TRUSTED_ORIGINS = ['https://ilpsummer.sarc-iitb.org', 'http://localhost:3001', 'http://127.0.0.1:8001', 'http://127.0.0.1:3001']