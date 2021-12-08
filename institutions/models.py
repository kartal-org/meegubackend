from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.utils.translation import gettext_lazy as _
from resources.models import InstitutionResourceFile
from products.models import Product
from members.models import BaseMember, BaseMemberType
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.exceptions import ObjectDoesNotExist
from subscriptions.models import InstitutionSubscription
from django.db.models.functions import Cast
from django.db.models import Sum, IntegerField
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django_currentuser.middleware import get_current_authenticated_user
from posts.models import Publication

from django.utils.text import slugify


def upload_to(instance, filename):
    return "products/image/{filename}".format(filename=filename)


def upload_verification(instance, filename):
    return "verifications/{filename}".format(filename=filename)


def upload_to_department(instance, filename):
    return "products/cover/department{filename}".format(filename=filename)


class Institution(Product):

    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(_("Profile"), upload_to=upload_to, default="userProfile/default_egry2i.jpg")
    address = models.TextField()
    contact = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    # staff =

    @property
    def is_Verified(self):
        # returns boolean
        try:
            status = InstitutionVerification.objects.get(institution=self.id, status="approved")
        except ObjectDoesNotExist:
            return False
        if status:
            return True

    @property
    def storage_Limit(self):
        # returns all storage bought through subscription
        limit = (
            InstitutionSubscription.objects.filter(institution=self.id)
            .annotate(storage_limit=Cast(KeyTextTransform("storage", "plan__limitations"), IntegerField()))
            .aggregate(Sum("storage_limit"))["storage_limit__sum"]
        )
        if limit == None:
            limit = 0
        return limit

    @property
    def storage_used(self):
        # how to compute? publication + resource
        publication = Publication.objects.filter(department__institution=self).aggregate(Sum("size"))["size__sum"]
        if publication == None:
            publication = 0

        resource = InstitutionResourceFile.objects.filter(folder__resource__institution=self).aggregate(Sum("size"))[
            "size__sum"
        ]

        if resource == None:
            resource = 0

        return publication + resource

    @property
    def storage_left(self):
        # returns all storage bought through subscription
        # institution = (
        #     InstitutionSubscription.objects.filter(institution=self)
        #     .annotate(storage_limit=Cast(KeyTextTransform("storage", "plan__limitations"), IntegerField()))
        #     .aggregate(Sum("storage_limit"))["storage_limit__sum"]
        # )
        limit = self.storage_Limit
        if limit == None:
            limit = 0
        used = self.storage_used
        if used == None:
            used = 0

        return limit - used

    @property
    def owner(self):
        # returns the owner of the institution
        return Staff.objects.get(institution=self.id, type__name="Creator").user.full_name

    # Hack to pass the user to post save signal.
    def save(self, *args, **kwargs):
        # Hack to pass the user to post save signal.
        self.current_authenticated_user = get_current_authenticated_user()
        super(Institution, self).save(*args, **kwargs)


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


class StaffType(BaseMemberType):
    custom_Type_For = models.ForeignKey(Institution, on_delete=CASCADE, null=True, blank=True)


class Staff(BaseMember):
    institution = models.ForeignKey(Institution, on_delete=CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.ForeignKey(StaffType, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ["user", "institution"]

    @property
    def institutions(self):
        return Institution.objects.filter(id=self.institution.id)

    def __str__(self):
        return "%s - %s" % (self.user.full_name, self.institution.name)


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


# signals
@receiver(post_save, sender=Institution)
def institution_create_owner(created, instance, *args, **kwargs):

    if created:

        defaultMember = Staff.objects.create(
            institution=instance, type=StaffType.objects.get(name="Admin"), user=instance.creator
        )
        defaultMember.save()


# signals
@receiver(pre_save, sender=Institution)
def institution_slug_pre_save(sender, instance, *args, **kwargs):

    if not instance.slug:
        instance.slug = slugify(instance.name)


# # signals
# @receiver(pre_save, sender=Institution)
# def department_slug_pre_save(sender, instance, *args, **kwargs):

#     if not instance.slug:
#         instance.slug = slugify(instance.name)
