from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from users.models import NewUser
import random


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"])
        # id start at 9
        def generate_username(fname, lname):
            # e.g. jonathanfisher2352
            return "%s%s%d" % (fname.lower(), lname.lower(), random.randint(1000, 9999))

        def default_password():
            return "QaxSf96H"
            pass

        for i in range(1, 10):
            # for i in range(87, 102):
            fname = fake.unique.first_name()
            lname = fake.unique.last_name()
            uname = generate_username(fname, lname)
            email = fake.unique.ascii_safe_email()
            password = default_password()
            about = fake.sentence()
            # NewUser.objects.create(
            #     first_name=fname, last_name=lname, username=uname, email=email, password=password, about=about
            # )
            print(i, fname, lname, uname, email, password, about)
