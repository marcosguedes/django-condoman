import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from apartments.models import Apartment
from dues.models import BankTransferDue, ExemptDue
from dues.utils import issue_due
from profiles.factory import UserFactory, ProprietorProfileFactory
from profiles.models import ProprietorProfile


# Create your tests here.
User = get_user_model()


class ProfileAccessTestCase(TestCase):
    def setUp(self):
        self.profiles = ProprietorProfileFactory.build_batch(10)

    def test_due_issuing(self):
        for profile in self.profiles:
            print(profile)


#         for proprietor in ProprietorProfile.objects.filter(
#             slug__in=User.objects.all().values_list(
#                 "proprietorprofile__slug", flat=True
#             )
#         ):
#             issue_due(proprietor)
#
#         self.assertEqual(ExemptDue.objects.all().count(), 1)
#         self.assertEqual(BankTransferDue.objects.all().count(), 1)
