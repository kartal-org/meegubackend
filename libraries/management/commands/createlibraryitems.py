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

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"]) 

        for _ in range(5):   
            userCount = NewUser.objects.count()
            user = NewUser.objects.get(id=random.randint(1,userCount))  
 
            publicationCount = Publication.objects.count()
            publication = Publication.objects.get(id=random.randint(1,publicationCount)) 

            LibraryItem.objects.create(
                owner=user, content=publication
            )
            print(user, publication)  
