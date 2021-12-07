from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from workspaces.models import WorkspaceFile
from submissions.models import Submission, Response, SubmissionResponse
from institutions.models import Department  
import random
from django.contrib.auth import authenticate, login 
 
SUBMISSIONFILE = Submission.objects.all()
TYPE = [
    "accepted",
    "revise", 
    "rejected", 
    "pending", 
]

class Provider(faker.providers.BaseProvider):
    def response_type(self):
        return self.random_element(TYPE) 
    
    def file_name(self):
        return self.random_element(SUBMISSIONFILE) 

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"]) 
        fake.add_provider(Provider) 
        
        for _ in SUBMISSIONFILE: 
            responseStatus = fake.response_type() 
            comment = fake.sentence()   
            file = fake.unique.file_name()  

            SubmissionResponse.objects.create(
                responseStatus=responseStatus, comment=comment, submission=file
            )
            print(responseStatus)  
