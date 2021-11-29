from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.utils import timezone
from files.models import Folder, QuillFile, UploadedFile, Package, File
from members.models import BaseMemberType, BaseMember
from classrooms.models import Classroom
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F


def upload_to(instance, filename):
    return "posts/{filename}".format(filename=filename)


class Workspace(Package):
    classroom = models.ForeignKey(Classroom, on_delete=CASCADE, null=True, blank=True)
    code = models.CharField(unique=True, max_length=8)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ["name", "classroom"]

    @property
    def members(self):
        return Member.objects.filter(workspace=self).values(
            uid=F("user__id"), first_name=F("user__first_name"), last_name=F("user__last_name")
        )


class MemberType(BaseMemberType):
    custom_Type_For = models.ForeignKey(Classroom, on_delete=CASCADE, null=True, blank=True)


class Member(BaseMember):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, null=True, blank=True, related_name="members")
    role = models.ForeignKey(MemberType, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ["user", "workspace"]

    def __str__(self):
        return "%s - %s" % (self.user.full_name, self.workspace.name)


@receiver(post_save, sender=Workspace)
def apply_verification_handler(created, instance, *args, **kwargs):
    if created:

        member = Member.objects.create(workspace=instance, role=MemberType.objects.get(pk=1), user=instance.creator)
        member.save()


class WorkspaceFolder(Folder):
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, blank=True, null=True, related_name="workspace_folder"
    )

    class Meta:
        unique_together = ["name", "workspace"]


class WorkspaceFile(File):
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
