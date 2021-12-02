from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from workspaces.models import WorkspaceFile
from submissions.models import Submission, Recommendation, RecommendationResponse
from institutions.models import Department  
import random
from django.contrib.auth import authenticate, login 
 
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

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"]) 
        fake.add_provider(Provider) 
        
        for _ in range(5): 
            responseStatus = fake.response_type() 
            comment = fake.sentence()   

            deptCount = Recommendation.objects.count()
            recommendation = Recommendation.objects.get(id=random.randint(1,deptCount))   

            RecommendationResponse.objects.create(
                responseStatus=responseStatus, comment=comment, recommendation=recommendation
            )
            print(responseStatus)  
