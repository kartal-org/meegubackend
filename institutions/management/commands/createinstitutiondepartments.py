from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers 
from institutions.models import Institution, Department
from users.models import NewUser
import random

INSTITUTIONS = Institution.objects.all() 
DEPARTMENTS = [
    "College of Arts and Sciences", 
    "College of Engineering",
    "College of Business",
    "College of Fine Arts and Communication",
    "College of Education",
]

class Provider(faker.providers.BaseProvider): 

    def institutions(self):
        return self.random_element(INSTITUTIONS)

    def departments(self):
        return self.random_element(DEPARTMENTS)
    

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"])  
        fake.add_provider(Provider)
         
        for x in INSTITUTIONS:  
            name = fake.unique.departments()
            description = fake.sentence() 

            institution = fake.institutions() 

            Department.objects.create(
                name=name, description=description, institution=institution
            ) 

            print(name, institution) 
        
