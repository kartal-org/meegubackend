from django.db import models
from django.conf import settings
from django.utils import timezone
from files.models import Folder, File


def upload_to(instance, filename):
    return "posts/{filename}".format(filename=filename)


class Workspace(models.Model):

    options = (("published", "Published"), ("draft", "Draft"))

    name = models.CharField(max_length=255)
    code = models.CharField(unique=True, max_length=8)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=options, default="draft")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    dateCreated = models.DateTimeField(default=timezone.now)
    dateUpdated = models.DateTimeField(default=timezone.now)

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
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="members_workspace")
    status = models.CharField(max_length=10, choices=options, default="accepted")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "workspace"]

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class WorkspaceFolder(Folder):
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, blank=True, null=True, related_name="workspace_folder"
    )

    class Meta:
        unique_together = ["name", "workspace"]


class WorkspaceFile(File):
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    class Meta:
        abstract = True


class WorkspaceQuillFile(WorkspaceFile):
    folder = models.ForeignKey(
        WorkspaceFolder,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    content = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ["name", "folder"]


class WorkspaceUploadedFile(WorkspaceFile):
    folder = models.ForeignKey(
        WorkspaceFolder,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    file = models.FileField(upload_to=upload_to)

    class Meta:
        unique_together = ["name", "folder"]
