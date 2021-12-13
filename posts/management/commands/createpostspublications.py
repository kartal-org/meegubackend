from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from institutions.models import Department
from posts.models import Category, Publication
from users.models import NewUser
from submissions.models import Submission
import random
import decimal
from django.contrib.auth import authenticate, login

DEPARTMENTS = Department.objects.all()
USERS = NewUser.objects.all()
SUBMISSIONS = Submission.objects.all()
TYPE = [
    {"file": "uploadedFiles/The_Image_of_The_Philippines_as_a_Tourism_Destination_in_Finland_xai3e0.pdf", "title":  "The Image of The Philippines as a Tourism Destination in Finland"},
    {"file": "uploadedFiles/Mother_Tongue-Based_Multilingual_Education_in_the_Philippines_apkzwn.pdf", "title":  "Mother Tongue-Based Multilingual Education in the Philippines"},
    {"file": "uploadedFiles/Difficulties_in_Remote_Learning_f7uwsx.pdf", "title":  "Difficulties in Remote Learning"},
    {"file": "uploadedFiles/Issues_and_Challenges_in_Open_and_Distance_e-Learning_nmast7.pdf", "title":  "Issues and Challenges in Open and Distance e-Learning"},
    {"file": "uploadedFiles/The_Impact_of_Peer_Binging_on_College_Student_brkxap.pdf", "title":  "The Impact of Peer Binging on College Student"},
]


class Provider(faker.providers.BaseProvider):
    def file_name(self):
        return self.random_element(TYPE)
    
    def department(self):
        return self.random_element(DEPARTMENTS)
    
    def user(self):
        return self.random_element(USERS)
    
    def submission(self):
        return self.random_element(SUBMISSIONS)


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"])
        fake.add_provider(Provider)

        for _ in SUBMISSIONS:

            title = fake.unique.sentence(nb_words=random.randint(1, 6))
            abstract = fake.unique.sentence() 
            department = fake.department()  
            user = fake.user()  
            archiveFile = fake.file_name()
            archiveAuthors = fake.unique.name()
 
            submission = fake.submission()

            Publication.objects.create(
                title=title,
                abstract=abstract,
                department=department, 
                archiveFile=archiveFile,
                archiveAuthors=archiveAuthors,
                submission=submission,
            )
            print(title, department, user)
