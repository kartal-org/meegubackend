from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from institutions.models import Institution, Department, Staff, StaffType
from users.models import NewUser
import random

USERS = NewUser.objects.all() 

class Provider(faker.providers.BaseProvider):
    def users(self):
        return self.random_element(USERS) 


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"])
        fake.add_provider(Provider)

        for _ in USERS:
            name = fake.unique.company() + " University"
            address = fake.address()
            contact = fake.numerify(text="############")
            email = fake.unique.ascii_company_email()
            website = fake.unique.domain_name()
            user = fake.unique.users()

            Institution.objects.create(
                name=name, address=address, contact=contact, email=email, website=website, creator=user
            )

            print(name, address, email)
 
            institution = Institution.objects.get(name=name) 
            type = StaffType.objects.get(name="Creator")

            Staff.objects.create(user=user, institution=institution, type=type)

            print(user, name)
