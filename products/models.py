from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from users.models import NewUser


def upload_to(instance, filename):
    return "products/cover/{filename}".format(filename=filename)


class PublicProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(privacy="public")


# This is the base model of the Classroom and Institution
class Product(models.Model):
    options = (("public", "Public"), ("private", "Private"))

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    privacy = models.CharField(max_length=10, choices=options, default="private")
    cover = models.ImageField(_("Cover"), upload_to=upload_to, default="userProfile/coverDefault_pdrisr.jpg")
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(NewUser, on_delete=models.CASCADE, null=True, blank=True)

    objects = models.Manager()  # default manager
    publicProduct = PublicProductManager()

    class Meta:
        ordering = ("-dateUpdated",)
        abstract = True

    def __str__(self):
        return self.name
