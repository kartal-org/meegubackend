from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from workspaces.models import WorkspaceFolder, WorkspaceFile
from workspaces.models import WorkspaceFile
from submissions.models import Submission  
import random
from django.contrib.auth import authenticate, login 
 
WORKSPACEFILE = WorkspaceFile.objects.all()

class Provider(faker.providers.BaseProvider):
    def file_name(self):
        return self.random_element(WORKSPACEFILE) 

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"])  
        fake.add_provider(Provider)
        
        for _ in range(5):
            title = fake.unique.bs() 
            description = fake.unique.sentence() 
            file = fake.file_name()   

            Submission.objects.create(
                title=title, description=description, file=file,
            )
            print(title)  
