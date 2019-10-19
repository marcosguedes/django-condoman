import datetime

from django.contrib.auth import get_user_model
import factory
from faker import Faker

from apartments.factory import ApartmentFactory

from . import models


User = get_user_model()

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    email = factory.Faker("email")
    is_staff = False
    is_active = False
    date_joined = factory.LazyFunction(datetime.datetime.now)

    class Meta:
        model = User


class ProprietorProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    apartment = factory.SubFactory(ApartmentFactory)
    phone = factory.Faker("phone_number")
    vat_number = factory.Faker("random_int", min=100000000, max=999999999)
    # vat_number = factory.LazyAttribute(lambda a: Faker.(min=100000000, max=999999999)))
    email_verified = factory.Faker("boolean")

    class Meta:
        model = models.ProprietorProfile


class ProprietorBillingAddressFactory(factory.django.DjangoModelFactory):
    proprietor = factory.SubFactory(ProprietorProfileFactory)
    name = factory.LazyAttribute(lambda a: "{0} {1}".format(a.first_name, a.last_name))
    address_1 = factory.Faker("street_name")
    address_2 = factory.Faker("secondary_address")
    postcode = factory.Faker("postcode")
    city = factory.Faker("city")
    vat_number = factory.Faker("random_int", min=100000000, max=999999999)

    class Meta:
        model = models.ProprietorBillingAddress
