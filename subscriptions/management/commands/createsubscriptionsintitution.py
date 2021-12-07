from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from subscriptions.models import Plan, Transaction, InstitutionSubscription
from institutions.models import Institution
import random
import decimal
from django.contrib.auth import authenticate, login

PLANS = Plan.objects.filter(type="institution")
INSTITUTIONS = Institution.objects.all()

class Provider(faker.providers.BaseProvider):
    def plans(self):
        return self.random_element(PLANS)
    
    def institutions(self):
        return self.random_element(INSTITUTIONS)
 
class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"]) 
        fake.add_provider(Provider)
        
        for _ in INSTITUTIONS:
            payer_Email = fake.unique.ascii_free_email() 
            payer_FullName = fake.unique.name() 
 
            plan = fake.plans()
             
            institution = fake.institutions()

            InstitutionSubscription.objects.create(
                payer_Email=payer_Email, payer_FullName=payer_FullName, plan=plan, institution=institution
            )
            print(payer_Email, plan, institution)  
