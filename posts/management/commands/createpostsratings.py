from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from institutions.models import Department
from posts.models import Category, Publication, Comment, Rating
from users.models import NewUser
from submissions.models import Submission
import random
import decimal
from django.contrib.auth import authenticate, login


PUBLICATIONS = Publication.objects.values_list("id", flat=True)


class Provider(faker.providers.BaseProvider):
    def publications(self):
        return self.random_element(PUBLICATIONS)


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"])
        fake.add_provider(Provider)

        # breakpoint()
        # # Create 50 ratings for all Publication
        # for i in range(51):
        #     rate = random.randint(1, 5)

        #     publication = fake.publications()
        #     publication = Publication.objects.get(id=random.randint(1, publicationCount))

        #     userCount = NewUser.objects.count()
        #     user = NewUser.objects.get(id=random.randint(1, userCount))

        #     Rating.objects.create(publication=publication, rate=rate, user=user)
        #     print(rate, publication, user)
