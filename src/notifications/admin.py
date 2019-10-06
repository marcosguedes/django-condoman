from django.contrib import admin
from .models import NotificationEmail

# Register your models here.

admin.site.register(NotificationEmail, admin.ModelAdmin)
