from django.db import models
from django.db.models.deletion import DO_NOTHING


# Create your models here.


class Plan(models.Model):
    options = (("classroom", "Classroom"), ("institution", "Institution"))
    statusOptions = (("active", "Active"), ("inactive", "Inactive"))

    class ClassroomPlans(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(type="classroom")

    class InstitutionPlans(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(type="institution")

    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(choices=statusOptions, default="active", max_length=10)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    limitations = models.JSONField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=options)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)

    objects = models.Manager()  # default manager
    classroomPlans = ClassroomPlans()  # custom manager
    institutionPlans = InstitutionPlans()  # custom manager

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ["name", "type"]


class Transaction(models.Model):
    payer_Email = models.EmailField()
    payer_FullName = models.CharField(max_length=255)
    plan = models.ForeignKey(Plan, on_delete=DO_NOTHING)
    dateCreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ClassroomSubscription(Transaction):
    classroom = models.ForeignKey("classrooms.Classroom", on_delete=DO_NOTHING)

    def __str__(self):
        return self.classroom.owner.full_name


class InstitutionSubscription(Transaction):
    institution = models.ForeignKey("institutions.Institution", on_delete=DO_NOTHING)

    def __str__(self):
        return self.institution.owner.full_name
