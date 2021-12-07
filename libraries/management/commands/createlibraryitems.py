from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from institutions.models import Department 
from posts.models import Category, Publication, Comment, Rating
from users.models import NewUser
from libraries.models import LibraryItem
import random
import decimal
from django.contrib.auth import authenticate, login  

PUBLICATIONS = Publication.objects.all()
USERS = NewUser.objects.all()

class Provider(faker.providers.BaseProvider):
    def publications(self):
        return self.random_element(PUBLICATIONS)
    
    def user(self):
        return self.random_element(USERS)

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"]) 
        fake.add_provider(Provider)

        for _ in PUBLICATIONS:    
            user = fake.user() 
            publication = fake.unique.publications()

            LibraryItem.objects.create(
                user=user, publication=publication
            )
            print(user, publication)  
