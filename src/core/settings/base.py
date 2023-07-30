"""
Django settings for MomsPops_API project.
"""
import os
from pathlib import Path

from .redis import REDIS_URL


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Server config
DEBUG = True
ALLOWED_HOSTS = ["*"]
SECRET_KEY = os.getenv("SECRET_KEY")


# Application definition
INSTALLED_APPS = [
    "daphne",
    # django utils
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # django applications
    "api",
    "users",
    "coordinates",
    "locations",
    "notifications",
    "profiles",
    "reactions",
    "chats",

    # libraries
    "channels",
    "rest_framework",
    "drf_yasg",
    "rest_framework_simplejwt",

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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


ASGI_APPLICATION = "core.asgi.application"
WSGI_APPLICATION = "core.wsgi.application"

# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")


# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = "media/"


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

TIME_FORMAT = r"%Y-%m-%d %H:%M:%S.%f %z"
