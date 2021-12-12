from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from users.models import NewUser
import random
from django.contrib.auth import authenticate, login

PROFILE_PICS = [
    "userProfile/pexels-amir-esrafili-6274712_txxmxu",
    "pexels-italo-melo-2379004_rz7vkx",
    "pexels-pixabay-220453_glwq6b",
    "pexels-andrea-piacquadio-774909_hkdg3j",
    "pexels-arthouse-studio-4571943_trdoog",
    "pexels-cottonbro-6195663_btbmtz",
    "pexels-pixabay-415829_gc8zlx",
]


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"])
        # for i in range(1, 10):
        for _ in range(15):
            fname = fake.unique.first_name()
            lname = fake.unique.last_name()
            uname = "%s%s%d" % (fname.lower(), lname.lower(), random.randint(1000, 9999))
            email = "%s@example.org" % (uname)
            # email = fake.unique.ascii_safe_email()
            password = "QaxSf96H"
            about = fake.sentence()

            NewUser.objects.create_user(
                first_name=fname, last_name=lname, username=uname, email=email, password=password, about=about
            )
            print(email, password)
