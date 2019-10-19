from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinLengthValidator
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _, gettext

from apartments.models import Apartment
from condofigurations.models import DEFAULT_COUNTRY, CondominiumConfiguration


class BaseProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False)
    vat_number = models.CharField(
        _("VAT Number"),
        help_text=_("Please ensure this number is correct. Numbers only"),
        null=True,
        blank=False,
        max_length=9,
        validators=[MinLengthValidator(9)],
    )
    notes = models.TextField(
        _("Internal Notes"),
        help_text=_("Internal Notes. Not publicly available"),
        blank=True,
    )
    email_verified = models.BooleanField("Email verified", default=False)

    class Meta:
        abstract = True

    @property
    def is_verified(self):
        return self.email_verified


@python_2_unicode_compatible
class ProprietorProfile(BaseProfile):
    """
    @summary: Before a proprietor has access to their information, their email/account
              must be verified
    """

    apartment = models.ForeignKey(Apartment, _("Apartment"), null=True)
    phone = models.CharField(_("Phone"), blank=True, max_length=100)
    due_exempt_until = models.DateTimeField(
        _("Exempt from dues until"),
        blank=True,
        null=True,
        help_text=_(
            "Date until proprietor is exempt from dues. Not publicly available.<br />\
            Exempt users will be issued exempted dues and won't be notified. \
            This normally happens when a proprietor is elected manager."
        ),
    )

    def __str__(self):
        return "{}".format(self.user)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ("user__name",)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("profiles:show", kwargs={"slug": self.slug})

    @property
    def is_exempt(self):
        try:
            return True if self.due_exempt_until >= timezone.now() else False
        except TypeError:
            return False

    @property
    def bill_same_address(self):
        """
        It's assumed the proprietor is a resident if they didn't filled
        in an address
        """
        try:
            return bool(self.address)
        except ProprietorBillingAddress.DoesNotExist:
            return True

    def billing_name(self):
        return self.address.name if not self.bill_same_address else self.user.name

    def billing_address_1(self):
        if not self.bill_same_address:
            return self.address.address_1

        return CondominiumConfiguration.get_solo().address_1

    def billing_address_2(self):
        if not self.bill_same_address:
            return self.address.address_2

        return CondominiumConfiguration.get_solo().address_2

    def billing_postcode(self):
        if not self.bill_same_address:
            return self.address.postcode

        return CondominiumConfiguration.get_solo().postcode

    def billing_city(self):
        if not self.bill_same_address:
            return self.address.city

        return CondominiumConfiguration.get_solo().city

    def billing_country(self):
        if not self.bill_same_address:
            return self.address.country

        return CondominiumConfiguration.get_solo().country

    def billing_vat_number(self):
        return self.vat_number if self.bill_same_address else self.address.vat_number

    @property
    def condominium_fee(self):
        try:
            return self.apartment.condominium_fee
        except AttributeError:
            # No apartment configured
            return None

    @property
    def condominium_fee_description(self):
        try:
            return self.apartment.condominium_fee_description
        except AttributeError:
            # No apartment configured
            return None


@python_2_unicode_compatible
class ProprietorBillingAddress(models.Model):
    """
    Address for receipts. Assume building address if proprietor has none.
    """

    proprietor = models.OneToOneField(
        ProprietorProfile, on_delete=models.CASCADE, related_name="address"
    )
    name = models.CharField(_("Name"), max_length=255)
    address_1 = models.CharField(_("Address 1"), max_length=400)
    address_2 = models.CharField(_("Address 2"), max_length=400, blank=True)
    postcode = models.CharField(_("Post Code"), max_length=100)
    city = models.CharField(_("City / Region"), max_length=100)
    country = models.CharField(_("Country"), max_length=400, default=DEFAULT_COUNTRY)
    vat_number = models.CharField(
        _("VAT number"),
        max_length=9,
        blank=True,
        help_text=_(
            "Leave empty if your VAT number is the same one you gave your profile"
        ),
    )

    def __str__(self):
        return gettext("{}'s address".format(self.user))

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ("proprietor",)
