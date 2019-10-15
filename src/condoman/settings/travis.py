import logging.config
import sys

from .base import *  # NOQA


ALLOWED_HOSTS = ["localhost"]
# tr -dc 'a-z0-9!@#$%^&*(-_=+)' < /dev/urandom | head -c50
SECRET_KEY = "s;>b6N[lW;Dg-gjb[gC>I/QoI1<<[Aaj3J[0mrUW>v%fO&@3wk"
STATIC_URL = "/static/"

DEBUG = True
TEMPLATES[0]["OPTIONS"].update({"debug": True})
# Show emails to console in DEBUG mode
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Show thumbnail generation errors
THUMBNAIL_DEBUG = True


if "TRAVIS" in os.environ:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "condoman",
            "USER": "postgres",
            "PASSWORD": "",
            "HOST": "localhost",
            "PORT": "",
        }
    }
