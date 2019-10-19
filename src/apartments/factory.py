import datetime
from random import randrange

import factory

from . import models


class ApartmentFactory(factory.django.DjangoModelFactory):
    fraction = factory.Faker("random_letter")
    floor = factory.Faker("random_digit")
    condominium_fee = factory.Faker("random_int", min=10, max=40)

    class Meta:
        model = models.Apartment
