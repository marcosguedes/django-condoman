from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _, gettext
from solo.models import SingletonModel


class CondominiumConfiguration(SingletonModel):

    condominium_fee = models.DecimalField(
        _("Condominium Fees"),
        max_digits=9,
        decimal_places=2,
        default="10.0",
        help_text=_("Value in Euros"),
    )
    condominium_payment_day = models.PositiveSmallIntegerField(
        _("Day"),
        validators=[MinValueValidator(1), MaxValueValidator(27)],
        help_text=_(
            "Payment Day. Choose a value from 1 to 27 in order to avoid issues with February and leaping years"
        ),
        default=1,
    )

    def __str__(self):
        return gettext("Condominium General Configuration")

    class Meta:
        verbose_name = _("Condominium General Configuration")
