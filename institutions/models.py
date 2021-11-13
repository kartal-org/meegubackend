from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from subscriptions.models import Plan
from files.models import Resource
from classrooms.models import Classroom


def upload_to(instance, filename):
    return "institutions/{filename}".format(filename=filename)


class Institution(models.Model):

    name = models.CharField(max_length=255)
    image = models.ImageField(_("Profile"), upload_to=upload_to, default="userProfile/default_egry2i.jpg")
    cover = models.ImageField(_("Cover"), upload_to=upload_to, default="userProfile/coverDefault_pdrisr.jpg")
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(default=timezone.now)
    dateUpdated = models.DateTimeField(default=timezone.now)

    objects = models.Manager()  # default manager

    class Meta:
        ordering = ("-dateUpdated",)

    def __str__(self):
        return self.name


class InstitutionSubscription(models.Model):
    institution = models.ForeignKey(Institution, on_delete=DO_NOTHING)
    plan = models.ForeignKey(Plan, on_delete=DO_NOTHING)
    payerName = models.CharField(max_length=255, blank=True, null=True)  # please remove null in deployment
    payerEmail = models.EmailField(max_length=254, blank=True, null=True)  # please remove null in deployment
    paidDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.payerName


class InstitutionVerification(models.Model):
    class VerifiedInstitution(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="approved")

    class PendingInstitution(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="pending")

    options = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("disapproved", "Disapproved"),
    )
    institution = models.OneToOneField(Institution, on_delete=CASCADE)
    status = models.CharField(max_length=20, choices=options, default="pending")
    document = models.FileField(upload_to=upload_to, null=True, blank=True)

    objects = models.Manager()  # default manager
    verified = VerifiedInstitution()  # custom manager
    pending = PendingInstitution()  # custom manager

    def __str__(self):
        return self.institution.name

    class Meta:
        ordering = ("-institution__dateUpdated",)


class StaffType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    permissions = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name


class CustomStaffType(StaffType):
    institution = models.ForeignKey(Institution, on_delete=CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)


class Staff(models.Model):
    options = (
        ("co-owner", "Co-Owner"),
        ("department-manager", "Department Manager"),
        ("adviser", "adviser"),
    )
    institution = models.ForeignKey(Institution, on_delete=CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.ForeignKey(StaffType, on_delete=models.SET_NULL, null=True, blank=True)


class InstitutionResource(Resource):
    institution = models.ForeignKey(Institution, on_delete=CASCADE)

    class Meta:
        unique_together = ["name", "institution"]
