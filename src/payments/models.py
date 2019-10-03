from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from . import PaymentStatus


class BasePayment(models.Model):
    status = models.CharField(
        max_length=10, choices=PaymentStatus.CHOICES, default=PaymentStatus.PENDING
    )
    description = models.CharField(_("Description"), max_length=400)
    value = models.DecimalField(
        _("Value"), max_digits=9, decimal_places=2, default="0.0"
    )
    billing_name = models.CharField(_("Name"), max_length=255)
    billing_address_1 = models.CharField(_("Billing Address 1"), max_length=400)
    billing_address_2 = models.CharField(
        _("Billing Address 2"), max_length=400, blank=True
    )
    billing_postcode = models.CharField(
        _("Billing Post Code"), max_length=100, blank=True
    )
    billing_city = models.CharField(
        _("Billing City / Region"), max_length=100, blank=True
    )
    billing_country = models.CharField(_("Billing Country"), max_length=400, blank=True)
    billing_vat_number = models.CharField(_("VAT number"), max_length=9)
    extra_data = models.TextField(_("Extra Data"), blank=True, default="")

    class Meta:
        abstract = True


class Payment(TimeStampedModel, BasePayment):
    pass

    class Meta:
        ordering = ("-created",)

    @classmethod
    def create_payment(
        cls,
        name,
        address_1,
        vat_number,
        value,
        description,
        address_2="",
        postcode="",
        city="",
        country="",
    ):
        obj = cls.objects.create(
            billing_name=name,
            value=value,
            description=description,
            billing_address_1=address_1,
            billing_address_2=address_2,
            billing_postcode=postcode,
            billing_city=city,
            billing_country=country,
            billing_vat_number=vat_number,
        )
        return obj
