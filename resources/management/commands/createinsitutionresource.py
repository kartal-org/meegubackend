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

class Provider(faker.providers.BaseProvider):
    def workspace_type(self):
        return self.random_element(TYPE) 

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"]) 
        fake.add_provider(Provider)
        
        for _ in range(5): 
            name = fake.unique.bs() 
            description = fake.unique.sentence() 
            status = fake.workspace_type() 

            institutionCount = Institution.objects.count()
            institution = Institution.objects.get(id=random.randint(1,institutionCount)) 

            deptCount = Department.objects.count()
            department = Department.objects.get(id=random.randint(1,deptCount)) 
 

            InstitutionResource.objects.create(
                name=name, description=description, status=status, institution=institution, department=department
            )
            print(name, status, institution, department)  
