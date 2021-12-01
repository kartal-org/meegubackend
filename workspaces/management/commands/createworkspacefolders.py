from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from workspaces.models import Workspace, WorkspaceFolder
from classrooms.models import Classroom
import random
import decimal
from django.contrib.auth import authenticate, login  

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"])  
        
        for _ in range(5): 
            name = fake.unique.bs()  

            wrkspaceCount = Workspace.objects.count()
            workspace = Workspace.objects.get(id=random.randint(1,wrkspaceCount)) 

            WorkspaceFolder.objects.create(
                name=name, workspace=workspace
            )
            print(name)  
