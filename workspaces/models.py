from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
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


def upload_to(instance, filename):
    return "posts/{filename}".format(filename=filename)


class Workspace(Package):
    classroom = models.ForeignKey("classrooms.Classroom", on_delete=CASCADE, null=True, blank=True)
    code = models.CharField(unique=True, max_length=8)

    class Meta:
        unique_together = ["name", "classroom"]

    @property
    def members(self):
        return Member.objects.filter(workspace=self).values(
            uid=F("user__user__id"), first_name=F("user__user__first_name"), last_name=F("user__user__last_name")
        )

    @property
    def storageUsed(self):
        return WorkspaceFile.objects.filter(folder__workspace=self).aggregate(Sum("size"))["size__sum"]

    # Hack to pass the user to post save signal.
    def save(self, *args, **kwargs):
        # Hack to pass the user to post save signal.
        self.current_authenticated_user = get_current_authenticated_user()
        super(Workspace, self).save(*args, **kwargs)


class Member(BaseMember):
    options = (
        ("member", "Member"),
        ("leader", "Leader"),
    )
    user = models.ForeignKey("classrooms.ClassroomMember", on_delete=models.CASCADE, blank=True, null=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=options, default="member")

    class Meta:
        unique_together = ["user", "workspace"]

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
        user = getattr(instance, "current_authenticated_user", None)
        print(user)
        breakpoint()
        classroomMember = apps.get_model("classrooms", "ClassroomMember")
        defaultMember = Member.objects.create(
            workspace=instance,
            role="leader",
            user=classroomMember.objects.get(classroom=instance.classroom, user=user),
        )
        defaultMember.save()
