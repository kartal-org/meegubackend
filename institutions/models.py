from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from subscriptions.models import Plan
from files.models import Package
from products.models import Product
from members.models import BaseMember


def upload_to(instance, filename):
    return "products/image/{filename}".format(filename=filename)


class Institution(Product):
    image = models.ImageField(_("Profile"), upload_to=upload_to, default="userProfile/default_egry2i.jpg")
    address = models.TextField()
    contact = models.CharField(max_length=11)
    email = models.EmailField()
    website = models.URLField(null=True, blank=True)


class StaffType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    custom_Type_For = models.ForeignKey(Institution, on_delete=CASCADE)

    def __str__(self):
        return self.name


class Staff(BaseMember):
    institution = models.ForeignKey(Institution, on_delete=CASCADE)
    type = models.ForeignKey(StaffType, on_delete=models.SET_NULL, null=True, blank=True)


# old
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


class InstitutionResource(Package):
    institution = models.ForeignKey(Institution, on_delete=CASCADE)

    class Meta:
        unique_together = ["name", "institution"]
