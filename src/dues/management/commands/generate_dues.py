import logging

from django.core.management.base import BaseCommand

from dues.models import ExemptDue, BankTransferDue
from profiles.models import ProprietorProfile


log = logging.getLogger(__name__)


def issue_due(proprietor):
    if proprietor.is_exempt:
        return ExemptDue.issue_due(proprietor)
    return BankTransferDue.issue_due(proprietor)


def generate_dues(dry_run=False):

    for proprietor in ProprietorProfile.objects.all():
        due = issue_due(proprietor)
        try:
            log.info("Due created for {}".format(due.name))
        except AttributeError:
            # No due created
            pass


class Command(BaseCommand):
    """
    This command should be run once a month on the same day the
    payment is issued. Periodicity should be controlled by crontab
    """

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--dry-run", action="store_true", help="Test Due generation"
        )

    def handle(self, *args, **options):
        log.info("Generating dues...")
        generate_dues(options["dry_run"])
