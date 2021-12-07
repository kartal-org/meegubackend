from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from resources.models import InstitutionResource
from institutions.models import Institution, Department 
import random
import decimal
from django.contrib.auth import authenticate, login 

TYPE = [
    "published",
    "draft", 
]
DEPARTMENT = Department.objects.all()
INSTITUTIONS = Institution.objects.all()

class Provider(faker.providers.BaseProvider):
    def department(self):
        return self.random_element(DEPARTMENT)
    
    def institution(self):
        return self.random_element(INSTITUTIONS)
        
    def workspace_type(self):
        return self.random_element(TYPE) 

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"]) 
        fake.add_provider(Provider)
        
        for _ in range(5): 

            name = fake.unique.bs() 
            description = fake.unique.sentence() 
            status = fake.workspace_type()  
            institution = fake.institution()  
            department = fake.department()  
 

            InstitutionResource.objects.create(
                name=name, description=description, status=status, institution=institution, department=department
            )
            print(name, status, institution, department)  
