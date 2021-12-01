from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers 
from institutions.models import Institution, Department, StaffType, Staff, InstitutionVerification
from users.models import NewUser
import random


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"]) 
        
        for _ in range(10):  
            institutionCount = Institution.objects.count()
            institution = Institution.objects.get(id=random.randint(1,institutionCount))

            document = "userProfile/coverDefault_pdrisr.jpg" 

            InstitutionVerification.objects.create(
                institution=institution, document=document
            ) 

            print(institution, document)  
