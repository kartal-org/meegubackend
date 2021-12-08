from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers 
from institutions.models import Institution, Department, StaffType, Staff
from users.models import NewUser
import random

USERS = NewUser.objects.all()
INSTITUTIONS = Institution.objects.all() 
DEPARTMENTS = Department.objects.all()
STAFFTYPE = StaffType.objects.all() 

class Provider(faker.providers.BaseProvider):
    def users(self):
        return self.random_element(USERS)

    def institutions(self):
        return self.random_element(INSTITUTIONS)
    
    def departments(self):
        return self.random_element(DEPARTMENTS)
    
    def stafftype(self):
        return self.random_element(STAFFTYPE)
          
class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"]) 
        fake.add_provider(Provider)
        
        for x in USERS: 
 
            user = fake.users()     
            institution = fake.unique.institutions()   
            department = fake.unique.departments()   
            type = fake.stafftype()  

            Staff.objects.create(
                user=user, institution=institution, department=department, type=type
            ) 

            print(user, institution)  
