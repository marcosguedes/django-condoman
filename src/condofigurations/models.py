from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _, gettext
from solo.models import SingletonModel


DEFAULT_COUNTRY = getattr(settings, "PROFILE_DEFAULT_COUNTRY", _("Portugal"))


class CondominiumConfiguration(SingletonModel):

    condominium_fee = models.DecimalField(
        _("Condominium Fees"),
        max_digits=9,
        decimal_places=2,
        default="10.0",
        help_text=_("Value in Euros"),
    )
    condominium_fee_description = models.CharField(
        _("Condominium Fee Description"),
        default=_("Condominium Fees"),
        help_text=_("Description for Invoices"),
        max_length=255,
    )
    payment_issue_day = models.PositiveSmallIntegerField(
        _("Payment Issuing Day"),
        validators=[MinValueValidator(1), MaxValueValidator(27)],
        help_text=_(
            "Day in the month where payment must be issued to a proprietor. \
            Choose a value from 1 to 27 in order to avoid issues with leaping years"
        ),
        default=1,
    )
    payment_issue_day_limit = models.PositiveSmallIntegerField(
        _("Payment Limit"),
        validators=[MinValueValidator(1)],
        help_text=_(
            "Number of days a due needs to be paid, including. User will be alerted once that moment passes.<br />\
            If Payment Issuing Day is set to August 4 and the payment limit is set to 5, the proprietor will \
            be alerted in August 10."
        ),
        default=5,
    )

    # Building address details. Will be used for resident proprietors
    address_1 = models.CharField(
        _("Address 1"), max_length=400, default="Sample Address 1"
    )
    address_2 = models.CharField(_("Address 2"), max_length=400, blank=True)
    postcode = models.CharField(
        _("Post Code"), max_length=100, default="Sample Postcode"
    )
    city = models.CharField(_("City / Region"), max_length=100, default="Sample City")
    country = models.CharField(_("Country"), max_length=400, default=DEFAULT_COUNTRY)

    def __str__(self):
        return gettext("Condominium General Configuration")

    class Meta:
        verbose_name = _("Condominium General Configuration")
