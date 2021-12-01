from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from workspaces.models import WorkspaceFile
from submissions.models import Submission, Recommendation
from institutions.models import Department  
import random
from django.contrib.auth import authenticate, login 
 
class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"])  
        
        for _ in range(5): 
            fileCount = Submission.objects.count()
            file = Submission.objects.get(id=random.randint(1,fileCount)) 

            deptCount = Department.objects.count()
            department = Department.objects.get(id=random.randint(1,deptCount)) 

            Recommendation.objects.create(
                submission=file, department=department, 
            )
            print(file, department)  
