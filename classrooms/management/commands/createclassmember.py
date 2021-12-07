from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from classrooms.models import Classroom, ClassroomMember
from users.models import NewUser
import random

USERS = NewUser.objects.all() 
CLASSROOMS = Classroom.objects.all()

class Provider(faker.providers.BaseProvider):
    def users(self):
        return self.random_element(USERS)
    
    def classrooms(self):
        return self.random_element(CLASSROOMS)

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"])
        fake.add_provider(Provider) 
        
        for x in CLASSROOMS:  
            member = fake.unique.users() 
            classroom = fake.unique.classrooms()  

            ClassroomMember.objects.create(
                user=member, classroom=classroom
            ) 
 
            print(member, classroom)  
