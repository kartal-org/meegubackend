from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.utils.translation import gettext_lazy as _
from products.models import Product
from members.models import BaseMember, BaseMemberType


def upload_to(instance, filename):
    return "products/image/{filename}".format(filename=filename)


def upload_verification(instance, filename):
    return "verifications/{filename}".format(filename=filename)


def upload_to_department(instance, filename):
    return "products/cover/department{filename}".format(filename=filename)


class Institution(Product):
    image = models.ImageField(_("Profile"), upload_to=upload_to, default="userProfile/default_egry2i.jpg")
    address = models.TextField()
    contact = models.CharField(max_length=11)
    email = models.EmailField()
    website = models.URLField(null=True, blank=True)


class StaffType(BaseMemberType):
    custom_Type_For = models.ForeignKey(Institution, on_delete=CASCADE, null=True, blank=True)


class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(_("Profile"), upload_to=upload_to_department, default="userProfile/default_egry2i.jpg")
    institution = models.ForeignKey(Institution, on_delete=CASCADE)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-dateModified",)
        unique_together = ["name", "institution"]

    def __str__(self):
        return self.name


class Staff(BaseMember):
    institution = models.ForeignKey(Institution, on_delete=CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.ForeignKey(StaffType, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ["user", "institution"]


class InstitutionVerification(models.Model):
    class VerifiedInstitution(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="approved")

    options = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("disapproved", "Disapproved"),
    )
    institution = models.OneToOneField(Institution, on_delete=CASCADE)
    status = models.CharField(max_length=20, choices=options, default="pending")
    document = models.FileField(upload_to=upload_verification, null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)

    objects = models.Manager()  # default manager
    verified = VerifiedInstitution()  # custom manager

    def __str__(self):
        return self.institution.name

    class Meta:
        ordering = ("-dateModified",)
