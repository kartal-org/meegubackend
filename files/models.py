from django.db import models
from django.db.models.deletion import CASCADE
from django.conf import settings
from django.utils.translation import gettext_lazy as _


def upload_to(instance, filename):
    return "uploadedFiles/{filename}".format(filename=filename)


def upload_cover_to(instance, filename):
    return "package-cover/{filename}".format(filename=filename)


# Create your models here.
class File(models.Model):
    options = (("published", "Published"), ("draft", "Draft"))
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=options, default="draft")
    tags = models.CharField(max_length=10, blank=True, null=True)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)
    size = models.PositiveIntegerField(default=0)
    file = models.FileField(upload_to=upload_to, null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Folder(models.Model):
    name = models.CharField(max_length=50)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        abstract = True

    def __str__(self):
        return self.name


class Package(models.Model):
    options = (("published", "published"), ("draft", "draft"))

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, max_length=255, null=True)
    status = models.CharField(max_length=10, choices=options, default="draft")
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)
    cover = models.ImageField(
        _("Cover"), upload_to=upload_cover_to, default="userProfile/coverDefault_pdrisr.jpg", null=True, blank=True
    )

    class Meta:
        abstract = True
        ordering = ("-dateUpdated",)

    def __str__(self):
        return self.name
