from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from workspaces.models import Workspace, WorkspaceFolder
from classrooms.models import Classroom
from users.models import NewUser
import random
import decimal
from django.contrib.auth import authenticate, login  

WORKSPACE = Workspace.objects.all()  

class Provider(faker.providers.BaseProvider):
    def workspace(self):
        return self.random_element(WORKSPACE)  

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"])  
        fake.add_provider(Provider)

        for _ in WORKSPACE: 

            name = fake.unique.bs()   
            workspace = fake.workspace()

            WorkspaceFolder.objects.create(
                name=name, workspace=workspace
            )
            print(name, workspace)  
