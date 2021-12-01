from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from notifications.models import Notification
from users.models import NewUser
import random
import decimal
from django.contrib.auth import authenticate, login


TYPE = [
    "verification",
    "submission", 
    "invitation", 
]

class Provider(faker.providers.BaseProvider):
    def notifs_type(self):
        return self.random_element(TYPE) 

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"])
        fake.add_provider(Provider)
        
        for _ in range(5):

            type = fake.notifs_type() 

            userCount = NewUser.objects.count()
            receiver = NewUser.objects.get(id=random.randint(1,userCount))  
            sender = NewUser.objects.get(id=random.randint(1,userCount)) 
 
            message = fake.unique.sentence()  

            Notification.objects.create(
                type=type, receiver=receiver, sender=sender, message=message
            )
            print(type, receiver, sender)  
