from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from institutions.models import Department 
from posts.models import Category, Publication, Comment, Rating
from users.models import NewUser
from submissions.models import Submission
import random
import decimal
from django.contrib.auth import authenticate, login  
 
USERS = NewUser.objects.all()
PUBLICATION = Publication.objects.all()

class Provider(faker.providers.BaseProvider):  
    def user(self):
        return self.random_element(USERS)
    
    def publication(self):
        return self.random_element(PUBLICATION)

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"])   
        fake.add_provider(Provider)

        for _ in PUBLICATION:   

            publication = fake.publication()   
            content = fake.sentence()  
            user = fake.user()  

            Comment.objects.create(
                publication=publication, content=content, user=user
            )
            print(publication, user)  
