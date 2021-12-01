from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers 
from institutions.models import Institution, Department
from users.models import NewUser
import random


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"])  

        for _ in range(10):  
            name = fake.unique.sentence(nb_words=2)
            description = fake.unique.sentence()

            institutionCount = Institution.objects.count()
            institution = Institution.objects.get(id=random.randint(1,institutionCount)) 

            Department.objects.create(
                name=name, description=description, institution=institution
            ) 

            print(name, institution) 
        
