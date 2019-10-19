from django.utils.translation import gettext_lazy as _
from dues.models import ExemptDue, BankTransferDue


def issue_due(proprietor):
    if proprietor.is_exempt:
        return ExemptDue.issue_due(proprietor)
    return BankTransferDue.issue_due(proprietor)
