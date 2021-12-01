from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers 
from workspaces.models import WorkspaceFolder, WorkspaceFile
from users.models import NewUser
import random
import decimal
from django.contrib.auth import authenticate, login  

TYPE = [
    "uploadedFiles/The_Image_of_The_Philippines_as_a_Tourism_Destination_in_Finland_xai3e0.pdf",
    "uploadedFiles/Mother_Tongue-Based_Multilingual_Education_in_the_Philippines_apkzwn.pdf",
    "uploadedFiles/Difficulties_in_Remote_Learning_f7uwsx.pdf",
    "uploadedFiles/Issues_and_Challenges_in_Open_and_Distance_e-Learning_nmast7.pdf",
    "uploadedFiles/The_Impact_of_Peer_Binging_on_College_Student_brkxap.pdf", 
]

class Provider(faker.providers.BaseProvider):
    def file_name(self):
        return self.random_element(TYPE) 

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"])  
        fake.add_provider(Provider)
        
        for _ in range(5): 
            name = fake.unique.bs()  
            
            tags = fake.unique.sentence(nb_words=2) 

            userCount = NewUser.objects.count()
            user = NewUser.objects.get(id=random.randint(1,userCount)) 
            
            file = fake.file_name() 
            content = fake.unique.sentence() 

            resourceCount = WorkspaceFolder.objects.count()
            resource = WorkspaceFolder.objects.get(id=random.randint(1,resourceCount)) 

            WorkspaceFile.objects.create(
                name=name, tags=tags, assignee=user, file=file, content=content, folder=resource
            )
            print(name, user, resource)  
