from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import gettext_lazy as _


class BaseProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False)
    # Add more user profile fields here. Make sure they are nullable
    # or with default values
    # picture = models.ImageField(
    #     "Profile picture", upload_to="profile_pics/%Y-%m-%d/", null=True, blank=True
    # )
    # bio = models.CharField("Short Bio", max_length=200, blank=True, null=True)
    vat_number = models.IntegerField(
        _("VAT Number"),
        help_text=_("Please ensure this number is correct. Numbers only"),
        null=True,
        blank=False,
        validators=[MaxValueValidator(999999999)],
    )
    notes = models.TextField(
        _("Internal Notes"),
        help_text=_("Internal Notes. Not publicly available"),
        blank=True,
    )
    email_verified = models.BooleanField("Email verified", default=False)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class ProprietorProfile(BaseProfile):
    fraction = models.CharField(_("Fraction"), max_length=100)
    apartment_number = models.CharField(_("Apartment no."), max_length=100)
    phone = models.CharField(_("Phone"), blank=True, max_length=100)

    def __str__(self):
        return "{}'s profile".format(self.user)
