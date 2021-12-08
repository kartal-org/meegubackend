from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from workspaces.models import WorkspaceFile
from submissions.models import Submission, Recommendation, RecommendationResponse
from institutions.models import Department  
import random
from django.contrib.auth import authenticate, login 
 
RECCOMENDATION = Recommendation.objects.all()
TYPE = [
    "accepted",
    "revise", 
    "rejected", 
    "pending", 
    "published", 
]

class Provider(faker.providers.BaseProvider):
    def response_type(self):
        return self.random_element(TYPE) 
    
    def recommendation(self):
        return self.random_element(RECCOMENDATION) 

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"]) 
        fake.add_provider(Provider) 
        
        for _ in range(5): 
            
            responseStatus = fake.response_type() 
            comment = fake.sentence()    
            recommendation = fake.recommendation()  

            RecommendationResponse.objects.create(
                responseStatus=responseStatus, comment=comment, recommendation=recommendation
            )
            print(responseStatus)  
