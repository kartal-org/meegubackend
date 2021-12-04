from django.core.management.base import BaseCommand
from posts.models import Category


CATEGORY_DEFAULTS = ["Sciences", "Technology", "Politics"]


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):

        for x in CATEGORY_DEFAULTS:

            Category.objects.create(name=x)
            print(x)
