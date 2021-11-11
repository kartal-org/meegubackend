from django.db import models

# Create your models here.
class Folder(models.Model):
    name = models.CharField(max_length=50)

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
