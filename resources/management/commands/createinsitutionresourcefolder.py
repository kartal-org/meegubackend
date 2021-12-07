from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers 
from resources.models import InstitutionResource, InstitutionResourceFolder
import random
import decimal
from django.contrib.auth import authenticate, login  

INSTITUTIONSRESOURCE = InstitutionResource.objects.all()

class Provider(faker.providers.BaseProvider): 
    
    def institution_resource(self):
        return self.random_element(INSTITUTIONSRESOURCE)

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"])  
        fake.add_provider(Provider)

        for _ in range(5): 

            name = fake.unique.bs()   
            resource = fake.institution_resource()   

            InstitutionResourceFolder.objects.create(
                name=name, resource=resource
            )
            print(name, resource)  

            
