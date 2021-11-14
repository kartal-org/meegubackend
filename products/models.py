from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


def upload_to(instance, filename):
    return "products/cover/{filename}".format(filename=filename)


# This is the base model of the Classroom and Institution
class Product(models.Model):
    options = (("public", "Public"), ("private", "Private"))
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    privacy = models.CharField(max_length=10, choices=options, default="private")
    cover = models.ImageField(_("Cover"), upload_to=upload_to, default="userProfile/coverDefault_pdrisr.jpg")
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    objects = models.Manager()  # default manager

    class Meta:
        ordering = ("-dateUpdated",)
        unique_together = (
            "owner",
            "name",
        )
        abstract = True

    def __str__(self):
        return self.name
