from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers 
from institutions.models import Institution, Department
from users.models import NewUser
import random
 
class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"]) 
        
        for _ in range(10):  
            name = fake.company()
            address = fake.address()
            contact = random.randint(11111111111,99999999999)
            email = fake.unique.ascii_company_email()
            website = fake.unique.domain_name()

            Institution.objects.create(
                name=name, address=address, contact=contact, email=email, website=website
            ) 

            print(name, address, email)  
        
