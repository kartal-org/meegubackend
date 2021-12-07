from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers 
from resources.models import ClassroomResource, ClassroomResourceFolder
import random
import decimal
from django.contrib.auth import authenticate, login  

CLASSROOMRESOURCE = ClassroomResource.objects.all() 

class Provider(faker.providers.BaseProvider):
    def classroom_resource(self):
        return self.random_element(CLASSROOMRESOURCE)

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"])  
        fake.add_provider(Provider)
        
        for _ in range(5): 

            name = fake.unique.bs()   
            resource = fake.classroom_resource()

            ClassroomResourceFolder.objects.create(
                name=name, resource=resource
            )
            print(name, resource)  
