from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _, gettext, gettext_noop
from django_extensions.db.models import TimeStampedModel
from post_office import mail
from post_office.models import Email, EmailTemplate


PAYMENT_ALERT_EMAIL_TEMPLATE = "payment_alert"  # Sent to owner
NEW_PAYMENT_EMAIL_TEMPLATE = "new_payment"  # Sent to admin
PAYMENT_PROCESSED_EMAIL_TEMPLATE = "payment_processed"  # Sent to owner


class NotificationEmail(TimeStampedModel):
    """
    Generic email notifications
    """

    STATUS_UNSENT = "unsent"
    STATUS_SENT = "sent"

    STATUS_CHOICES = (
        (STATUS_UNSENT, gettext_noop("Unsent")),
        (STATUS_SENT, gettext_noop("Sent")),
    )

    EMAIL_TEMPLATE_CHOICES = getattr(
        settings,
        "NOTIFICATION_EMAIL_TEMPLATES",
        (
            (PAYMENT_ALERT_EMAIL_TEMPLATE, gettext_noop("Payment Alert")),
            (NEW_PAYMENT_EMAIL_TEMPLATE, gettext_noop("New Payment")),
            (PAYMENT_PROCESSED_EMAIL_TEMPLATE, gettext_noop("Payment Processed")),
        ),
    )
    status = models.CharField(
        _("Status"), choices=STATUS_CHOICES, default=STATUS_UNSENT, max_length=100
    )
    recipient = models.EmailField(_("Recipient"), max_length=255)
    template = models.CharField(
        _("Subject"), max_length=255, choices=EMAIL_TEMPLATE_CHOICES, blank=True
    )
    subject = models.CharField(_("Subject"), max_length=255, blank=True)
    message = models.TextField(_("Message"), max_length=255, blank=True)

    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.SET_NULL
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = gettext("Notification Email")
        verbose_name_plural = gettext("Notification Emails")
        ordering = ("-created",)

    def __str__(self):
        if self.subject:
            return "(%s) %s" % (self.recipient, self.subject)
        return self.recipient

    @property
    def is_sent(self):
        return True if self.status is self.STATUS_SENT else False

    @classmethod
    def create_notification(
        cls,
        recipient,
        template="",
        subject="",
        message="",
        context_dict=None,
        send_mail=False,
    ):
        notif = cls(recipient)

        if not context_dict:
            raise ValueError("Notification has no context dictionary.")

        if template:
            try:
                notif.template = EmailTemplate.objects.get(name=template)
            except EmailTemplate.DoesNotExist:
                raise ValueError("Template with name `%s` doesn't exist" % template)

        elif not all([subject, message]):
            raise ValueError(
                "Notification needs a template or a subject and a message."
            )

        notif.subject = subject
        notif.message = message

        notif.save()

        if send_mail:
            notif.send_mail(context_dict)
        return notif

    def send_mail(self, context_dict):

        email = mail.send(
            self.recipient,
            getattr(settings, "DEFAULT_FROM_EMAIL", None),
            self.template,
            context_dict,
        )
        self.status = self.STATUS_SENT
        self.save()
