from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers 
from resources.models import ClassroomResource, ClassroomResourceFolder, ClassroomResourceFile
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

USERS = NewUser.objects.all()
CLASSROOMRESOURCEFOLDER = ClassroomResourceFolder.objects.all()

class Provider(faker.providers.BaseProvider):
    def user(self):
        return self.random_element(USERS)
    
    def classroomresource_folder(self):
        return self.random_element(CLASSROOMRESOURCEFOLDER)
         
    def file_name(self):
        return self.random_element(TYPE) 

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"])  
        fake.add_provider(Provider)
        
        for _ in range(5): 

            name = fake.unique.bs()  
            tags = fake.unique.sentence(nb_words=1)  
            user = fake.user()   
            file = fake.file_name() 
            content = fake.unique.sentence()  
            resource = fake.classroomresource_folder() 

            ClassroomResourceFile.objects.create(
                name=name, tags=tags, assignee=user, file=file, content=content, folder=resource
            )
            print(name, user, resource)  
