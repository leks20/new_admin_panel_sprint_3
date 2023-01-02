import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings
from split_settings.tools import include

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = "5432"

    DJANGO_LOG_LEVEL: str = "INFO"

    PAGE_SIZE: str = "50"

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()

SECRET_KEY = (os.environ.get("SECRET_KEY"),)

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEBUG = os.environ.get("DEBUG", False) == "True"

ALLOWED_HOSTS = [
    "*",
]
LOCALE_PATHS = [
    "movies/locale",
]
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8080",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": settings.POSTGRES_DB,
        "USER": settings.POSTGRES_USER,
        "PASSWORD": settings.POSTGRES_PASSWORD,
        "HOST": settings.POSTGRES_SERVER,
        "PORT": settings.POSTGRES_PORT,
        "OPTIONS": {"options": "-c search_path=public,content"},
    }
}

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "default": {
            "format": "%(levelname)s : %(asctime)s {%(module)s} [%(funcName)s] %(message)s - [in line № %(lineno)d]",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "filters": ["require_debug_true"],
        },
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": settings.DJANGO_LOG_LEVEL,
            "propagate": False,
        },
    },
}

include(
    "components/middleware.py",
    "components/installed_apps.py",
    "components/internationalization.py",
    "components/templates.py",
    "components/password_validation.py",
)
