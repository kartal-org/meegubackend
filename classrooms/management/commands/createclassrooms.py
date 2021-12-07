from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from classrooms.models import Classroom, ClassroomMember
from institutions.models import Institution, Department, StaffType, Staff
from users.models import NewUser
import random

USERS = NewUser.objects.all() 
INSTITUTIONS = Institution.objects.all()
SUBJECTS = [
    "Biology",
    "Chemistry and Biochemistry",
    "Computer Science",
    "Earth and Space Sciences",
    "English and Modern Languages",
    "History",
    "Mathematics",
    "Physics",
    "Political Science",
    "Psychology",
]

class Provider(faker.providers.BaseProvider):
    def users(self):
        return self.random_element(USERS) 

    def institutions(self):
        return self.random_element(INSTITUTIONS) 

    def subjects(self):
        return self.random_element(SUBJECTS) 
    
class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"]) 
        fake.add_provider(Provider)

        for _ in USERS:
            name = fake.unique.bs() 
            description = fake.unique.sentence() 
            code = fake.password(length=8, special_chars=False)
            subject = fake.unique.subjects()  
 
            institution = fake.institutions()
            user = fake.unique.users()  

            Classroom.objects.create(
                name=name, description=description, code=code, subject=subject, institution=institution, creator=user
            )  
            print(code, subject)  

            # member = fake.unique.users() 
            classroom = Classroom.objects.get(name=name)   

            ClassroomMember.objects.create(
                user=user, classroom=name, role="adviser"
            ) 

            print(member, classroom)  
         
