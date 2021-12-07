from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers 
from institutions.models import Institution, Department, StaffType, Staff, InstitutionVerification
from users.models import NewUser
import random

INSTITUTIONS = Institution.objects.all() 

class Provider(faker.providers.BaseProvider): 

    def institutions(self):
        return self.random_element(INSTITUTIONS)


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"]) 
        fake.add_provider(Provider)
        
        for x in INSTITUTIONS:   
            institution = fake.unique.institutions() 
            document = "userProfile/coverDefault_pdrisr.jpg" 

            InstitutionVerification.objects.create(
                institution=institution, document=document
            ) 

            print(institution, document)  
