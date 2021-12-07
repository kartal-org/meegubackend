from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from workspaces.models import WorkspaceFile
from submissions.models import Submission, Recommendation
from institutions.models import Department  
import random
from django.contrib.auth import authenticate, login 

SUBMISSIONFILE = Submission.objects.all()
DEPARTMENT = Department.objects.all()

class Provider(faker.providers.BaseProvider):
    def file_name(self):
        return self.random_element(SUBMISSIONFILE) 

    def department(self):
        return self.random_element(DEPARTMENT) 

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["en_US"])  
        fake.add_provider(Provider)

        for _ in SUBMISSIONFILE:  
            file = fake.unique.file_name() 
            department = fake.department()

            Recommendation.objects.create(
                submission=file, department=department, 
            )
            print(file, department)  
