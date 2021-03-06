from django.db import models
from django.conf import settings
from workspaces.models import Workspace, WorkspaceFile

# from institutions.models import Institution
from products.models import Product
from members.models import BaseMember, BaseMemberType
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django_currentuser.middleware import get_current_authenticated_user
from django.db.models.functions import Cast
from django.db.models import Sum, IntegerField
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from subscriptions.models import ClassroomSubscription, InstitutionSubscription
from resources.models import ClassroomResourceFile
from django.core.exceptions import ObjectDoesNotExist
from institutions.models import Institution

from django.apps import apps


class Classroom(Product):
    code = models.CharField(max_length=8, unique=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    institution = models.ForeignKey(Institution, null=True, blank=True, on_delete=models.SET_NULL)

    # Hack to pass the user to post save signal.
    def save(self, *args, **kwargs):
        # Hack to pass the user to post save signal.
        self.current_authenticated_user = get_current_authenticated_user()
        super(Classroom, self).save(*args, **kwargs)

    @property
    def subscriptions(self):
        return ClassroomSubscription.objects.filter(classroom=self.id).values("id")

    @property
    def adviser(self):
        return ClassroomMember.objects.get(classroom=self.id, role="adviser").user.full_name

    @property
    def adviserInstance(self):
        return ClassroomMember.objects.get(classroom=self.id, role="adviser").user

    @property
    def storage_Limit(self):
        # returns all storage bought through subscription
        institutionStorageLeft = 0
        if self.institution:
            institutionStorageLeft = self.institution.storage_left
        classroom = (
            ClassroomSubscription.objects.filter(classroom=self.id)
            .annotate(storage_limit=Cast(KeyTextTransform("storage", "plan__limitations"), IntegerField()))
            .aggregate(Sum("storage_limit"))["storage_limit__sum"]
        )
        if not classroom:
            classroom = 0
        return classroom + institutionStorageLeft

    @property
    def storage_used(self):
        workspace = WorkspaceFile.objects.filter(folder__workspace__classroom=self).aggregate(Sum("size"))["size__sum"]
        if workspace == None:
            workspace = 0

        resource = ClassroomResourceFile.objects.filter(folder__resource__classroom=self).aggregate(Sum("size"))[
            "size__sum"
        ]

        if resource == None:
            resource = 0

        return workspace + resource

    @property
    def storage_left(self):
        # returns all storage bought through subscription
        classroom = (
            ClassroomSubscription.objects.filter(classroom=self.id)
            .annotate(storage_limit=Cast(KeyTextTransform("storage", "plan__limitations"), IntegerField()))
            .aggregate(Sum("storage_limit"))["storage_limit__sum"]
        )
        if classroom == None:
            classroom = 0
        institution = 0
        if self.institution:
            institution = self.institution.storage_left

        return classroom + institution - self.storage_used


class ClassroomMember(BaseMember):
    options = (("adviser", "Adviser"), ("student", "Student"))
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="members")
    role = models.CharField(max_length=10, choices=options, default="student")

    class Meta:
        unique_together = ["user", "classroom"]

    @property
    def classrooms(self):
        return Classroom.objects.filter(id=self.classroom.id)
        # .values(
        #     "id", "name", "description", "code", "cover", "privacy"
        # )

    def __str__(self):
        return "%s - %s" % (self.user.full_name, self.classroom.name)


# signals
@receiver(post_save, sender=Classroom)
def classroom_create_adviser(created, instance, *args, **kwargs):
    if created:
        # breakpoint()
        defaultMember = ClassroomMember.objects.create(classroom=instance, role="adviser", user=instance.creator)
        defaultMember.save()
