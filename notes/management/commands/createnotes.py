from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers 
from notes.models import Note
from users.models import NewUser
import random


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"]) 
        
        for _ in range(10):  
            title = fake.sentence(nb_words=4)
            content = fake.sentence()

            userCount = NewUser.objects.count()
            user = NewUser.objects.get(id=random.randint(1,userCount)) 

            Note.objects.create(
                title=title, content=content, owner=user
            ) 

            print(title, user)  
