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

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"]) 

        for _ in range(5):  
            rate = random.randint(1,5)

            publicationCount = Publication.objects.count()
            publication = Publication.objects.get(id=random.randint(1,publicationCount))  

            userCount = NewUser.objects.count()
            user = NewUser.objects.get(id=random.randint(1,userCount))  

            Rating.objects.create(
                publication=publication, rate=rate, user=user
            )
            print(rate, publication, user)  
