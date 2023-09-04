"""
Django settings for liveconfigs_example project.

Generated by 'django-admin startproject' using Django 3.2.20.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

import dj_database_url
import environ

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-#yqyyn9t4$etmejs!fi!j!lbd5x9(wz^gmv98jep((o%6+nv4h"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "more_admin_filters",
    "import_export",
    "django_extensions",
    "django_celery_beat",
    "simpleapp.apps.SimpleappConfig",
    "liveconfigs",
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

ROOT_URLCONF = "liveconfigs_example.urls"

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

WSGI_APPLICATION = "liveconfigs_example.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default="postgres://{}:{}@{}:{}/{}".format(
            env("DJANGO_POSTGRES_USER", default="admin"),
            env("DJANGO_POSTGRES_PASSWORD", default="password"),
            env("DJANGO_POSTGRES_HOST", default="postgres"),
            env("DJANGO_POSTGRES_PORT", default="5432"),
            env("DJANGO_POSTGRES_DB", default="liveconfigs_db"),
        ),
    ),
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
        "standard": {
            "format": "%(asctime)s %(levelname)s [%(name)s: %(lineno)s] -- %(message)s",
            "datefmt": "%m-%d-%Y %H:%M:%S",
        },
        "json": {"()": "log_utils.JsonFormatter"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "json"
            if env("HOST_NAME", default="localhost") != "localhost"
            else "simple",
        },
    },
    "loggers": {
        "": {
            "handlers": [
                "console",
            ],
            "level": "DEBUG",
            "propagate": False,
        },
        "django": {
            "handlers": [
                "console",
            ],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.db.backends": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
    },
}

# celery settings
broker_transport_options = {"visibility_timeout": 3600}
result_backend = env("CELERY_BROKER_URL", default="redis://redis:6379/0")
task_track_started = True
task_serializer = "pickle"
result_serializer = "pickle"
accept_content = ["pickle"]

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"

CELERY_TASK_ROUTES = {
    "configs.configs.config_row_update_or_create_proxy": {
        "queue": "quick",
        "routing_key": "quick",
    },
}

# redis settings
REDIS_BASE_URL = env("REDIS_BASE_URL", default="redis://redis:6379")

CACHES = {
    "redis_cache": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS_BASE_URL}/1",
        "TIMEOUT": 864000,
        "OPTIONS": {
            "MAX_ENTRIES": 1000,
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "redis_cache_pricing": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS_BASE_URL}/2",
        "TIMEOUT": 300,
        "OPTIONS": {
            "MAX_ENTRIES": 1000,
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    },
}

# liveconfigs settings
# Максимальная длина текста в значении конфига при которой отображать поле редактирования конфига как textinput
# При длине текста в значении конфига большей этого значения - отображать поле редактирования конфига как textarea
LC_MAX_STR_LENGTH_DISPLAYED_AS_TEXTINPUT = 50
LC_ENABLE_PRETTY_INPUT = True
LIVECONFIGS_SYNCWRITE = True    # sync write mode