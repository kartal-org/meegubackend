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

            classCount = Classroom.objects.count()
            classroom = Classroom.objects.get(id=random.randint(1,classCount)) 

            institutionCount = Institution.objects.count()
            institution = Institution.objects.get(id=random.randint(1,institutionCount)) 

            ClassroomResource.objects.create(
                name=name, description=description, status=status, classroom=classroom, institution=institution
            )
            print(name, status, classroom, institution)  
