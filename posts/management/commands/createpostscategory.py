from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from posts.models import Category 
from django.contrib.auth import authenticate, login 

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"]) 
        
        for _ in range(5):
            name = fake.unique.sentence(nb_words=2) 

            Category.objects.create(
                name=name
            )
            print(name)  
