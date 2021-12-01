from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from subscriptions.models import Plan, Transaction, InstitutionSubscription
from institutions.models import Institution
import random
import decimal
from django.contrib.auth import authenticate, login


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"]) 
        
        for _ in range(5):
            payer_Email = fake.unique.ascii_free_email() 
            payer_FullName = fake.unique.name() 

            planCount = Plan.objects.count()
            plan = Plan.objects.get(id=random.randint(1,planCount))
            
            insitutionCount = Institution.objects.count()
            institution = Institution.objects.get(id=random.randint(1,insitutionCount)) 

            InstitutionSubscription.objects.create(
                payer_Email=payer_Email, payer_FullName=payer_FullName, plan=plan, institution=institution
            )
            print(payer_Email, plan, institution)  
