from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from workspaces.models import Workspace, Member
from users.models import NewUser
from classrooms.models import ClassroomMember
import random
import decimal
from django.contrib.auth import authenticate, login 

CLASSROOMMEMBER = ClassroomMember.objects.all()
WORKSPACE = Workspace.objects.all()

class Provider(faker.providers.BaseProvider):
    def workspace(self):
        return self.random_element(WORKSPACE) 

    def classroommember(self):
        return self.random_element(CLASSROOMMEMBER) 

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"])  
        fake.add_provider(Provider)
        
        for _ in CLASSROOMMEMBER:    
            member = fake.unique.classroommember() 
            workspace = fake.unique.workspace()

            Member.objects.create(
                user=member, workspace=workspace
            )
            print(member, workspace)  
