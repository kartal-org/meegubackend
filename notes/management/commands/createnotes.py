from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers 
from notes.models import Note
from users.models import NewUser
import random

USERS = NewUser.objects.all()  

class Provider(faker.providers.BaseProvider):
    def users(self):
        return self.random_element(USERS)  
    
class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"]) 
        fake.add_provider(Provider)

        for _ in range(10):  
            title = fake.unique.sentence(nb_words=4)
            content = fake.sentence() 
            user = fake.users() 

            Note.objects.create(
                title=title, content=content, owner=user
            ) 

            print(title, user)  
