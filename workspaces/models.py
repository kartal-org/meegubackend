from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.utils import timezone
from files.models import Folder, QuillFile, UploadedFile, Package
from members.models import BaseMemberType, BaseMember
from classrooms.models import Classroom


def upload_to(instance, filename):
    return "posts/{filename}".format(filename=filename)


class Workspace(Package):
    classroom = models.ForeignKey(Classroom, on_delete=CASCADE, null=True, blank=True)
    code = models.CharField(unique=True, max_length=8)

    class Meta:
        unique_together = ["name", "classroom"]


class MemberType(BaseMemberType):
    custom_Type_For = models.ForeignKey(Classroom, on_delete=CASCADE, null=True, blank=True)


class Member(BaseMember):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(MemberType, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ["user", "workspace"]


class WorkspaceFolder(Folder):
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, blank=True, null=True, related_name="workspace_folder"
    )

    class Meta:
        unique_together = ["name", "workspace"]


class WorkspaceQuillFile(QuillFile):
    folder = models.ForeignKey(
        WorkspaceFolder,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    class Meta:
        unique_together = ["name", "folder"]


class WorkspaceUploadedFile(UploadedFile):
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
