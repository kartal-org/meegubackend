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
            name = fake.unique.bs() 
            description = fake.unique.sentence() 
            code = fake.unique.pystr() 
            subject = fake.unique.company()  

            Classroom.objects.create(
                name=name, description=description, code=code, subject=subject
            )  
            print(code, subject)  

#note: need to comment out the classroom creator signal in models  
