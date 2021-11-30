from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from users.models import NewUser
import random
from django.contrib.auth import authenticate, login


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"])
        # for i in range(1, 10):
        # for i in range(87, 102):
        fname = fake.unique.first_name()
        lname = fake.unique.last_name()
        uname = "%s%s%d" % (fname.lower(), lname.lower(), random.randint(1000, 9999))
        email = fake.unique.ascii_safe_email()
        password = "QaxSf96H"
        about = fake.sentence()
        NewUser.objects.create_user(
            first_name=fname, last_name=lname, username=uname, email=email, password=password, about=about
        )
        print(email, password)
