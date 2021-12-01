from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers 
from institutions.models import Institution, Department, StaffType, Staff
from users.models import NewUser
import random


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"]) 
        
        for _ in range(10): 

            userCount = NewUser.objects.count()
            user = NewUser.objects.get(id=random.randint(1,userCount))   

            institutionCount = Institution.objects.count()
            institution = Institution.objects.get(id=random.randint(1,institutionCount))

            departmentCount = Department.objects.count()
            department = Department.objects.get(id=random.randint(1,departmentCount))   

            staffTypeCount = StaffType.objects.count()
            type = StaffType.objects.get(id=random.randint(1,staffTypeCount))  

            Staff.objects.create(
                user=user, institution=institution, department=department, type=type
            ) 

            print(user, institution)  
