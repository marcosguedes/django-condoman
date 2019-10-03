from django.utils.translation import pgettext_lazy


class PaymentStatus:
    PENDING = "pending"
    WAITING = "waiting"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"

    CHOICES = [
        (PENDING, pgettext_lazy("payment status", "Pending")),
        (WAITING, pgettext_lazy("payment status", "Waiting for confirmation")),
        (CONFIRMED, pgettext_lazy("payment status", "Confirmed")),
        (REJECTED, pgettext_lazy("payment status", "Rejected")),
    ]
