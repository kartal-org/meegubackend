from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers 
from workspaces.models import Workspace
from classrooms.models import Classroom, ClassroomMember
from users.models import NewUser
import random
import decimal
from django.contrib.auth import authenticate, login 

USERS = NewUser.objects.all()
CLASSROOMS = Classroom.objects.all() 
TYPE = [
    "published",
    "draft", 
]

class Provider(faker.providers.BaseProvider):
    def workspace_type(self):
        return self.random_element(TYPE) 

    def classrooms(self):
        return self.random_element(CLASSROOMS) 

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"]) 
        fake.add_provider(Provider)
        
        for _ in CLASSROOMS: 
            name = fake.unique.bs() 
            description = fake.sentence() 
            status = fake.workspace_type()  
            classroom = fake.unique.classrooms()

            code = fake.password(length=8, special_chars=False)
            creator = ClassroomMember.objects.get(classroom=classroom, role="adviser")

            Workspace.objects.create(
                name=name, description=description, status=status, classroom=classroom, code=code, creator=creator
            )
            print(name, status, classroom)   
            