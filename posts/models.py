from django.db import models
from django.conf import settings

# from institutions.models import Department
from workspaces.models import WorkspaceFile
from submissions.models import Submission

# from institutions.models import Institution
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.db.models import F
from django.db.models.functions import Cast
from django.db.models import Sum, IntegerField, Avg
from django.contrib.postgres.fields.jsonb import KeyTextTransform


# Create your models here.
def upload_to(instance, filename):
    return "posts/{filename}".format(filename=filename)


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Publication(models.Model):
    options = (("public", "Public"), ("private", "Private"))
    title = models.TextField(max_length=250, unique=True)
    abstract = models.TextField()
    slug = models.SlugField(max_length=250, null=True, blank=True)
    privacy = models.CharField(choices=options, default="public", max_length=10)
    department = models.ForeignKey("institutions.Department", on_delete=models.CASCADE, null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True, related_name="categories")
    is_featured = models.BooleanField(default=False)
    publishedDate = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)
    archiveFile = models.FileField(upload_to=upload_to, null=True, blank=True)
    archiveAuthors = models.TextField(null=True, blank=True)
    submission = models.ForeignKey(Submission, on_delete=models.PROTECT, blank=True, null=True)
    size = models.PositiveBigIntegerField(default=0)

    @property
    def institution(self):
        if self.department:
            return self.department.institution.id

    @property
    def authors(self):
        if self.archiveFile:
            return self.archiveAuthors
        if self.submission:
            return self.submission.file.file.workspace.members

    @property
    def file(self):
        if self.archiveFile:
            return self.archiveFile
        if self.submission:
            return self.submission.file.file

    @property
    def rating(self):
        return Rating.objects.filter(publication=self.id).aggregate(Avg("rate"))["rate__avg"]

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Publication)
def slug_pre_save(sender, instance, *args, **kwargs):

    if not instance.slug:
        instance.slug = slugify(instance.title)


class Comment(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-dateUpdated",)

    def __str__(self):
        return "%s - %s (%s)" % (self.user.username, self.publication.title, self.dateUpdated)


class Rating(models.Model):
    options = ((1, "Very Bad"), (2, "Bad"), (3, "Average"), (4, "Good"), (5, "Very Good"))
    rate = models.IntegerField(choices=options)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, blank=True, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "publication"]
        ordering = ("-dateUpdated",)

    def __str__(self):
        return "%s - %s (%d)" % (self.user.full_name, self.publication.title, self.rate)
