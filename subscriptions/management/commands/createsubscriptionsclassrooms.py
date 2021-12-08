from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from subscriptions.models import Plan, Transaction, ClassroomSubscription
from classrooms.models import Classroom
import random
import decimal
from django.contrib.auth import authenticate, login

PLANS = Plan.objects.all().filter(type="classroom")
CLASSROOMS = Classroom.objects.all()

class Provider(faker.providers.BaseProvider):
    def plans(self):
        return self.random_element(PLANS)

    def classrooms(self):
        return self.random_element(CLASSROOMS)
 
class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"]) 
        fake.add_provider(Provider)
        
        for _ in CLASSROOMS:
            payer_Email = fake.unique.ascii_free_email() 
            payer_FullName = fake.unique.name()  
            plan = fake.plans() 
            classroom = fake.classrooms()  

            ClassroomSubscription.objects.create(
                payer_Email=payer_Email, payer_FullName=payer_FullName, plan=plan, classroom=classroom
            )
            print(payer_Email, plan, classroom)  
