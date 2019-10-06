from django.contrib import admin

# Register your models here.
from .models import BankTransferDue, ExemptDue


@admin.register(BankTransferDue)
class BankTransferDueAdmin(admin.ModelAdmin):
    list_display = ("name", "proprietor", "payment", "payment_date_limit")


@admin.register(ExemptDue)
class ExemptDueAdmin(admin.ModelAdmin):
    list_display = ("name", "proprietor", "payment")
