from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from subscriptions.models import Plan, Transaction, ClassroomSubscription
from classrooms.models import Classroom
import random
import decimal
from django.contrib.auth import authenticate, login


TYPE = [
    "Classroom",
    "Institution", 
]

class Provider(faker.providers.BaseProvider):
    def subscription_type(self):
        return self.random_element(TYPE) 

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"])
        fake.add_provider(Provider)
        
        for _ in range(5):
            name = fake.unique.bs() 
            description = fake.unique.sentence()  
            price = float(random.randrange(155, 5089))/100
            type = fake.subscription_type() 

            Plan.objects.create(
                name=name, description=description, price=price, type=type
            )
            print(name, price, type)  
