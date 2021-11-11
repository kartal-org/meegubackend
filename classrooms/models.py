from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from files.models import Folder, File


def upload_to(instance, filename):
    return "classroom/{filename}".format(filename=filename)


class Classroom(models.Model):
    class PublishedClassrooms(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="published")

    options = (("published", "Published"), ("draft", "Draft"))

    name = models.CharField(max_length=255)
    code = models.CharField(unique=True, max_length=8)
    subject = models.CharField(max_length=255, null=True, blank=True)
    section = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=options, default="draft")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    dateCreated = models.DateTimeField(default=timezone.now)
    dateUpdated = models.DateTimeField(default=timezone.now)

    objects = models.Manager()  # default manager
    publishedClassrooms = PublishedClassrooms()  # custom manager

    class Meta:
        ordering = ("-dateUpdated",)

    def __str__(self):
        return self.name


class Member(models.Model):
    options = (
        ("accepted", "accepted"),
        ("rejected", "rejected"),
        ("pending", "pending"),
    )
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="members")
    status = models.CharField(max_length=10, choices=options, default="accepted")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_member")

    class Meta:
        unique_together = ["student", "classroom"]

    def __str__(self):
        return self.student.first_name + " " + self.student.last_name


class Resource(models.Model):
    options = (("published", "published"), ("draft", "draft"))

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, max_length=255)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=10, choices=options, default="draft")
    dateCreated = models.DateTimeField(default=timezone.now)
    dateUpdated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-dateUpdated",)

    def __str__(self):
        return self.name


class ClassroomResourceFolder(Folder):
    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, blank=True, null=True, related_name="source_resource_folder"
    )

    class Meta:
        unique_together = ["name", "resource"]


class ClassroomResourceQuillFile(File):
    folder = models.ForeignKey(
        ClassroomResourceFolder,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    content = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ["name", "folder"]


class ClassroomResourceUploadedFile(File):
    folder = models.ForeignKey(
        ClassroomResourceFolder,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    file = models.FileField(upload_to=upload_to)

    class Meta:
        unique_together = ["name", "folder"]
