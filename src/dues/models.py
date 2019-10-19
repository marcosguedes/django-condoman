import datetime
import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _, gettext
from django_extensions.db.models import TimeStampedModel

from payments import PaymentStatus
from payments.models import Payment
from profiles.models import ProprietorProfile


log = logging.getLogger(__name__)


class BaseDue(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    slug = models.UUIDField(_("Slug"), default=uuid.uuid4)
    proprietor = models.ForeignKey(
        ProprietorProfile,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_dues",
    )
    payment = models.ForeignKey(
        Payment, null=True, on_delete=models.SET_NULL, related_name="%(class)s_dues"
    )

    class Meta:
        abstract = True

    @classmethod
    def issue_payment(cls, proprietor):
        """
        Create a payment object
        """
        payment = Payment.create_payment(
            name=proprietor.billing_name(),
            address_1=proprietor.billing_address_1(),
            address_2=proprietor.billing_address_2(),
            postcode=proprietor.billing_postcode(),
            city=proprietor.billing_city(),
            country=proprietor.billing_country(),
            vat_number=proprietor.billing_vat_number(),
            value=proprietor.condominium_fee,
            description=proprietor.condominium_fee_description,
        )
        return payment

    @classmethod
    def issue_due(cls, proprietor):
        raise NotImplementedError


class BankTransferDue(TimeStampedModel, BaseDue):
    image = models.ImageField(
        # Required but null in order to automatically create a due. The proprietor will
        # then upload proof of payment at a later date
        _("Image"),
        upload_to="dues/%Y-%m-%d/",
        null=True,
    )
    # payment_date_limit is informative, not coercive. Limit will change on post_save
    payment_date_limit = models.DateTimeField(
        _("Payment Date Limit"), default=timezone.now
    )

    class Meta:
        verbose_name = gettext("Bank Transfer Due")
        verbose_name_plural = gettext("Bank Transfer Dues")
        ordering = ("-created",)

    @classmethod
    def issue_due(cls, proprietor):
        if not proprietor.apartment:
            log.warning(
                "Owner {} doesn't have an apartment value set. Payment not issued.".format(
                    proprietor
                )
            )
            return None

        from condofigurations.models import CondominiumConfiguration

        config = CondominiumConfiguration.get_solo()
        payment = cls.issue_payment(proprietor)
        due = cls.objects.create(
            name=proprietor.billing_name(),
            proprietor=proprietor,
            payment=payment,
            payment_date_limit=timezone.now()
            + datetime.timedelta(days=config.payment_issue_day_limit),
        )
        return due


class ExemptDue(TimeStampedModel, BaseDue):
    """
    Some people are exempt from their dues due to services provided
    for the building (normally Managers). Will be issued a payment set as Paid
    """

    class Meta:
        ordering = ("-created",)
        verbose_name = gettext("Exempt Due")
        verbose_name_plural = gettext("Exempt Dues")

    @classmethod
    def issue_due(cls, proprietor):
        if not proprietor.apartment:
            log.warning(
                "Owner {} doesn't have an apartment value set. Payment not issued.".format(
                    proprietor
                )
            )
            return None

        payment = cls.issue_payment(proprietor)
        payment.value = 0
        payment.status = PaymentStatus.CONFIRMED
        payment.save()

        due = cls.objects.create(
            name=proprietor.billing_name(), proprietor=proprietor, payment=payment
        )
        return due
