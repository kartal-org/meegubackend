from django.db import models
from django.conf import settings

from django.utils import timezone
from files.models import Folder, Package, File
from members.models import BaseMemberType, BaseMember

# from classrooms.models import Classroom, ClassroomMember
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django_currentuser.middleware import get_current_authenticated_user

from django.db.models.functions import Cast
from django.db.models import Sum, IntegerField
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.apps import apps
from users.models import NewUser
import shortuuid


def upload_to(instance, filename):
    return "posts/{filename}".format(filename=filename)


class Workspace(Package):

    classroom = models.ForeignKey("classrooms.Classroom", on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(unique=True, max_length=8, null=True, blank=True)
    creator = models.ForeignKey("classrooms.ClassroomMember", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ["name", "classroom"]
        # ordering = ("-dateModified",)

    @property
    def storageUsed(self):
        return WorkspaceFile.objects.filter(folder__workspace=self).aggregate(Sum("size"))["size__sum"]

    # # Hack to pass the user to post save signal.
    # def save(self, *args, **kwargs):
    #     # Hack to pass the user to post save signal.
    #     self.current_authenticated_user = get_current_authenticated_user()
    #     super(Workspace, self).save(*args, **kwargs)


class Member(BaseMember):
    options = (("leader", "Leader"), ("member", "Member"))
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=options, default="member")
    user = models.ForeignKey("classrooms.ClassroomMember", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "workspace"]

    @property
    def username(self):
        return self.user.user.username

    # @property
    # def workspaces(self):
    #     return Workspace.objects.filter(id=self.workspace.id).values("id")

    def __str__(self):
        return "%s - %s" % (self.user.user.full_name, self.workspace.name)


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


@receiver(post_save, sender=Workspace)
def workspace_create_leader(created, instance, *args, **kwargs):

    if created:
        classroomMember = apps.get_model("classrooms", "ClassroomMember")
        Member.objects.create(
            user=classroomMember.objects.get(user=instance.creator.user, classroom=instance.classroom),
            workspace=instance,
        )


@receiver(post_save, sender=Workspace)
def workspace_create_resource_folder(created, instance, *args, **kwargs):

    if created:
        WorkspaceFolder.objects.create(workspace=instance, name="Resources")


def get_code():
    codeID = shortuuid.ShortUUID().random(length=8)
    return codeID


@receiver(pre_save, sender=Workspace)
def slug_pre_save(sender, instance, *args, **kwargs):

    if not instance.code:
        instance.code = get_code()
