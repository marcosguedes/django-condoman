# admin.py

from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import CondominiumConfiguration

admin.site.register(CondominiumConfiguration, SingletonModelAdmin)
