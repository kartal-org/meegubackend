from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from workspaces.models import WorkspaceFile
from submissions.models import Submission  
import random
from django.contrib.auth import authenticate, login 
 
class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"])  
        
        for _ in range(5):
            title = fake.unique.sentence(nb_words=6) 
            description = fake.unique.sentence()
 
            fileCount = WorkspaceFile.objects.count()
            file = WorkspaceFile.objects.get(id=random.randint(1,fileCount)) 

            status = fake.submission_type() 

            Submission.objects.create(
                title=title, description=description, file=file, status=status, 
            )
            print(title, status)  
