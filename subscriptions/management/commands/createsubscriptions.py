from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from subscriptions.models import Plan, Transaction, ClassroomSubscription
from classrooms.models import Classroom
import random
import decimal
from django.contrib.auth import authenticate, login


TYPE = [
    "classroom",
    "institution",
]


class Provider(faker.providers.BaseProvider):
    def subscription_type(self):
        return self.random_element(TYPE)


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"])
        fake.add_provider(Provider)
        # {"storage": 5000000}

        Plan.objects.create(
            name="Classroom Basic", 
            description="Free One Time Subscription Plan For Classroom.", 
            type="classroom"
        )
        Plan.objects.create(
            name="Classroom Upgrade 1",
            description="Extend 5GB to your Classroom Storage",
            price=50.00,
            type="classroom",
        )
        Plan.objects.create(
            name="Classroom Upgrade 2",
            description="Extend 5GB to your Classroom Storage",
            price=50.00,
            type="classroom",
            limitations={"storage": 10000000},
        )
        Plan.objects.create(
            name="Institution Basic", description="Free One Time Subscription Plan For Institution.", type="institution"
        )
        Plan.objects.create(
            name="Institution Upgrade 1",
            description="Extend 5GB to your Institution Storage",
            price=50.00,
            type="institution",
        )
        Plan.objects.create(
            name="Institution Upgrade 2",
            description="Extend 5GB to your Institution Storage",
            price=50.00,
            type="institution",
            limitations={"storage": 10000000},
        )

        # for _ in range(5):
        #     name = fake.unique.bs()
        #     description = fake.unique.sentence()
        #     price = float(random.randrange(155, 5089))/100
        #     type = fake.subscription_type()

        #     Plan.objects.create(
        #         name=name, description=description, price=price, type=type
        #     )
        #     print(name, price, type)
