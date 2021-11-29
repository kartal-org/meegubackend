from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from classrooms.models import Classroom
import random


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        fake = Faker(["tl_PH"])

        for i in range(87, 102):

            print()
            pass
