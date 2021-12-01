from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from workspaces.models import Workspace, Member
from users.models import NewUser
from classrooms.models import ClassroomMember
import random
import decimal
from django.contrib.auth import authenticate, login 

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"])  
        
        for _ in range(5):   
            classmemberCount = ClassroomMember.objects.count()
            member = ClassroomMember.objects.get(id=random.randint(1,classmemberCount)) 

            wrkspaceCount = Workspace.objects.count()
            workspace = Workspace.objects.get(id=random.randint(1,wrkspaceCount))  

            Member.objects.create(
                user=member, workspace=workspace
            )
            print(member, workspace)  
