import logging
from django.core.management.base import BaseCommand
from django.utils import timezone

from condofigurations.models import CondominiumConfiguration
from dues.models import BankTransferDue, ExemptDue
from profiles.models import ProprietorProfile

log = logging.getLogger("project")


def generate_dues(dry_run=False):
    config = CondominiumConfiguration.get_solo()

    if config.payment_issue_day != timezone.now().day:
        return

    today = timezone.now().date()

    current_month_dues = BankTransferDue.objects.filter(created__date=today)
    current_exempt_month_dues = ExemptDue.objects.filter(created__date=today)

    processed_proprietor_ids = list(
        current_month_dues.values_list("proprietor__slug", flat=True)
    ) + list(current_exempt_month_dues.values_list("proprietor__slug", flat=True))

    unprocessed_proprietors = ProprietorProfile.objects.all().exclude(
        slug__in=processed_proprietor_ids
    )

    for proprietor in unprocessed_proprietors:
        if proprietor.is_exempt:
            log.info("Issuing an exempt due for {}".format(proprietor))
            if dry_run:
                log.info("[Dry Run] Issued to {}".format(proprietor))
            else:
                ExemptDue.issue_payment(proprietor)
            continue

        log.info("Issuing a bank transfer due for {}".format(proprietor))
        if dry_run:
            log.info("[Dry Run] Issued to {}".format(proprietor))
        else:
            BankTransferDue.issue_payment(proprietor)


class Command(BaseCommand):
    """
    This command should be run once a month on the same day the
    payment is issued. Shouldn't even have a check and allow issuing everytime it ran
    :todo: find out if it makes sense or if it should be programatically controlled
    """

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--dry-run", action="store_true", help="Test Due generation"
        )

    def handle(self, *args, **options):
        log.info("Generating dues...")
        generate_dues(options["dry_run"])
