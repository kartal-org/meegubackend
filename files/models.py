from django.db import models
from django.db.models.deletion import CASCADE
from django.conf import settings


# Create your models here.
class Folder(models.Model):
    name = models.CharField(max_length=50)
    institution = models.ForeignKey(
        "institutions.Institution",
        on_delete=CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("name",)
        unique_together = ["name", "resource"]
        abstract = True

    def __str__(self):
        return self.name


class File(models.Model):
    options = (("published", "Published"), ("draft", "Draft"))
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=options, default="draft")
    tags = models.CharField(max_length=10, blank=True, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class UploadedFile(File):
    size = models.PositiveIntegerField()


class Resource(models.Model):
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
