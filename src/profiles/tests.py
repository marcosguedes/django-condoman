from __future__ import unicode_literals

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from profiles.models import ProprietorProfile


class PageOpenTestCase(TestCase):
    def test_home_page_exists(self):
        url = reverse("home")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)

    def test_about_page_exists(self):
        url = reverse("about")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)


User = get_user_model()


class ProfileTestCase(TestCase):
    from django.conf import settings

    def setUp(self):
        self.verified_user_credentials = {
            "email": "veridummy@example.com",
            "password": "secret",
        }
        self.unverified_user_credentials = {
            "email": "unveridummy@example.com",
            "password": "secret",
        }
        self.verified_user = User.objects.create_user(**self.verified_user_credentials)
        self.unverified_user = User.objects.create_user(
            **self.unverified_user_credentials
        )
        self.verified_user.proprietorprofile.email_verified = True
        self.verified_user.proprietorprofile.save()

    def access_profile_pages(self):
        unauthenticated_client = Client()
        unverified_client = Client()
        verified_client = Client()
        unverified_client.login(
            email=self.unverified_user_credentials["email"],
            password=self.unverified_user_credentials["password"],
        )
        verified_client.login(
            email=self.verified_user_credentials["email"],
            password=self.verified_user_credentials["password"],
        )
        for proprietor in ProprietorProfile.objects.all():

            # Unauthenticated users must be redirected to login
            self.assertEqual(
                unauthenticated_client.get(proprietor.get_absolute_url()).status_code,
                302,
            )
            # Throw error to unauthorized users except if they're accessing their own page
            self.assertEqual(
                unverified_client.get(proprietor.get_absolute_url()).status_code,
                200
                if proprietor is auth.get_user(unverified_client).proprietorprofile
                else 403,
                "User {} can't access page belonging to {}".format(
                    auth.get_user(unverified_client), proprietor.user
                ),
            )
            # Verified users can access each other's pages, unverified or not
            self.assertEqual(
                verified_client.get(proprietor.get_absolute_url()).status_code, 200
            )
