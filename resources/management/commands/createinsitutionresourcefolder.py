from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers 
from resources.models import InstitutionResource, InstitutionResourceFolder
import random
import decimal
from django.contrib.auth import authenticate, login  

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"])  
        
        for _ in range(5): 
            name = fake.unique.bs()  

            resourceCount = InstitutionResource.objects.count()
            resource = InstitutionResource.objects.get(id=random.randint(1,resourceCount)) 

            InstitutionResourceFolder.objects.create(
                name=name, resource=resource
            )
            print(name, resource)  
