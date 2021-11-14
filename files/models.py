from django.db import models
from django.db.models.deletion import CASCADE
from django.conf import settings


# Create your models here.
class File(models.Model):
    options = (("published", "Published"), ("draft", "Draft"))
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=options, default="draft")
    tags = models.CharField(max_length=10, blank=True, null=True)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


def upload_to(instance, filename):
    return "uploadedFiles/{filename}".format(filename=filename)


class UploadedFile(File):
    size = models.PositiveIntegerField(default=0)
    file = models.FileField(upload_to=upload_to)

    class Meta:
        abstract = True


class QuillFile(File):
    content = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class Folder(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ("name",)
        abstract = True

    def __str__(self):
        return self.name


class Package(models.Model):
    options = (("published", "published"), ("draft", "draft"))

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, max_length=255)
    status = models.CharField(max_length=10, choices=options, default="draft")
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-dateUpdated",)

    def __str__(self):
        return self.name
