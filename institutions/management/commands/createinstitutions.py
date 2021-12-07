from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers 
from institutions.models import Institution, Department, Staff, StaffType
from users.models import NewUser
import random
 
USERS = NewUser.objects.all() 
DEPARTMENTS = Department.objects.all()

class Provider(faker.providers.BaseProvider):
    def users(self):
        return self.random_element(USERS)  
    
    def departments(self):
        return self.random_element(DEPARTMENTS) 
 
class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"]) 
        fake.add_provider(Provider)
        
        for x in USERS:  
            name = fake.company()
            address = fake.address()
            contact = fake.numerify(text='############')
            email = fake.unique.ascii_company_email()
            website = fake.unique.domain_name()
            user = fake.users()  

            Institution.objects.create(
                name=name, address=address, contact=contact, email=email, website=website, creator=user
            ) 

            print(name, address, email)  

            user = fake.users()     
            institution = Institution.objects.get(name=name)   
            department = fake.unique.departments()   
            type =  StaffType.objects.get(name="Admin")    

            Staff.objects.create(
                user=user, institution=institution, department=department, type=type
            ) 

            print(user, institution)  
        
