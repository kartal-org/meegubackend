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

TYPE = [
    "uploadedFiles/The_Image_of_The_Philippines_as_a_Tourism_Destination_in_Finland_xai3e0.pdf",
    "uploadedFiles/Mother_Tongue-Based_Multilingual_Education_in_the_Philippines_apkzwn.pdf",
    "uploadedFiles/Difficulties_in_Remote_Learning_f7uwsx.pdf",
    "uploadedFiles/Issues_and_Challenges_in_Open_and_Distance_e-Learning_nmast7.pdf",
    "uploadedFiles/The_Impact_of_Peer_Binging_on_College_Student_brkxap.pdf",
]


class Provider(faker.providers.BaseProvider):
    def file_name(self):
        return self.random_element(TYPE)


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"])
        fake.add_provider(Provider)

        for _ in range(5):
            title = fake.unique.sentence(nb_words=random.randint(1, 6))
            abstract = fake.unique.sentence()

            deptCount = Department.objects.count()
            department = Department.objects.get(id=random.randint(1, deptCount))

            # # start category pending
            # deptCount = Category.objects.count()
            # category = Category.objects.get(id=random.randint(1, deptCount))
            # category.save()
            # category.name.add(category)
            # # end

            userCount = NewUser.objects.count()
            user = NewUser.objects.get(id=random.randint(1, userCount))

            content = fake.unique.sentence()

            archiveFile = fake.file_name()
            archiveAuthors = fake.unique.name()

            submissionCount = Submission.objects.count()
            submission = Submission.objects.get(id=random.randint(1, submissionCount))

            Publication.objects.create(
                title=title,
                abstract=abstract,
                department=department,
                # user=user,
                # content=content,
                archiveFile=archiveFile,
                archiveAuthors=archiveAuthors,
                submission=submission,
            )
            print(title, department, user)
