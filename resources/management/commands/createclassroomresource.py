from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from resources.models import ClassroomResource
from institutions.models import Institution
from classrooms.models import Classroom
import random
import decimal
from django.contrib.auth import authenticate, login 

TYPE = [
    "published",
    "draft", 
]
CLASSROOMS = Classroom.objects.all()
INSTITUTIONS = Institution.objects.all()

class Provider(faker.providers.BaseProvider):
    def classroom(self):
        return self.random_element(CLASSROOMS)
    
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
            classroom = fake.classroom()  
            institution = fake.institution() 

            ClassroomResource.objects.create(
                name=name, description=description, status=status, classroom=classroom, institution=institution
            )
            print(name, status, classroom, institution)  
