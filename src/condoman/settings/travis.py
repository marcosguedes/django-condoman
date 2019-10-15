import logging.config
import sys

from .base import *  # NOQA


ALLOWED_HOSTS = ["localhost"]
# tr -dc 'a-z0-9!@#$%^&*(-_=+)' < /dev/urandom | head -c50
SECRET_KEY = "s;>b6N[lW;Dg-gjb[gC>I/QoI1<<[Aaj3J[0mrUW>v%fO&@3wk"
STATIC_URL = "/static/"

DEBUG = True

if "TRAVIS" in os.environ:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "travisci",
            "USER": "postgres",
            "PASSWORD": "",
            "HOST": "localhost",
            "PORT": "",
        }
    }
