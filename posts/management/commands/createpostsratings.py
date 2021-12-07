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

        fake = Faker(["tl_PH"])
        fake.add_provider(Provider)
 
        for i in USERS:
            rate = random.randint(1, 5) 
            publication = fake.publications()   
            user = fake.unique.user() 

            Rating.objects.create(publication=publication, rate=rate, user=user)
            print(rate, publication, user)
