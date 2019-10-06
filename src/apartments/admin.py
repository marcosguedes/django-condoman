from django.contrib import admin

# Register your models here.
from .models import Apartment


@admin.register(Apartment)
class BankTransferDueAdmin(admin.ModelAdmin):
    list_display = ("fraction", "floor", "condominium_fee")
    list_editable = ("condominium_fee",)
