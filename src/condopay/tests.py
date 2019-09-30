from __future__ import unicode_literals

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .models import Payment


class PaymentTestCase(TestCase):
    def test_payment_creation(self):
        payment = Payment.objects.create(
            description="Book purchase",
            value=Decimal(20),
            billing_name="John Doe",
            billing_address_1="Avenida Infante D. Henrique, 40",
            billing_vat=000000000,
        )
        print(payment, payment.value)
        self.assertEqual(
            20, payment.value, _("Payment was not created with the expected value")
        )
