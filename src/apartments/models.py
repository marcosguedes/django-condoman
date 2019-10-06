from django.db import models
from django.utils.translation import gettext_lazy as _, gettext


class Apartment(models.Model):
    fraction = models.CharField(_("Fraction"), max_length=100)
    floor = models.CharField(_("Floor"), max_length=100)
    # Should observations be used to keep a record of an apartment's issues?
    observations = models.TextField(_("Observations"), blank=True)
    condominium_fee = models.DecimalField(
        _("Condominium Fee"),
        max_digits=9,
        decimal_places=2,
        default="10.0",
        help_text="Value in Euros",
    )
    order = models.PositiveSmallIntegerField(
        _("Order"), default=0, editable=False
    )  # Fraction name should handle ordering. If not, order will

    class Meta:
        verbose_name = gettext("Apartment")
        verbose_name_plural = gettext("Apartments")
        ordering = ("order", "fraction")

    @property
    def name(self):
        return "%s / %s" % (self.fraction, self.floor)

    def __str__(self):
        return self.name
