from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from classrooms.models import Classroom, ClassroomMember
from users.models import NewUser
import random


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"]) 
        
        for _ in range(10):  
            userCount = NewUser.objects.count()
            member = NewUser.objects.get(id=random.randint(1,userCount))

            classCount = Classroom.objects.count()
            classroom = Classroom.objects.get(id=random.randint(1,classCount)) 

            ClassroomMember.objects.create(
                user=member, classroom=classroom
            ) 

            print(member, classroom)  
