from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from institutions.models import Institution, StaffType 
from users.models import NewUser
import random


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"]) 
        
        for _ in range(10):  
            name = fake.sentence(nb_words=2)
            description = fake.sentence() 
            
            institutionCount = Institution.objects.count()
            institution = Institution.objects.get(id=random.randint(1,institutionCount))

            StaffType.objects.create(
                name=name, description=description, custom_Type_For=institution
            ) 

            print(name, institution)  
