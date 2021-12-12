from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from institutions.models import Institution, StaffType
from users.models import NewUser
import random

STAFF_TYPES = [
    {"name": "Creator", "description": "Institution Page's Owner. Has all the rights to manage the Page"},
    {"name": "Admin", "description": "Institution Page's Owner. Has all the rights to manage the Page"},
    {
        "name": "Department Head",
        "description": "Institution Department's Head. Has all the rights to manage the department",
    },
    {"name": "Adviser", "description": "Has the right to make recommendations"},
    {"name": "Publisher", "description": "Has the right to make publication in the department"},
]


class Provider(faker.providers.BaseProvider):
    def staff_types(self):
        return self.random_element(STAFF_TYPES)


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"])
        fake.add_provider(Provider)

        for x in STAFF_TYPES:

            StaffType.objects.create(name=x["name"], description=x["description"])
            print(x["name"])
