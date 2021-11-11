from django.db import models

# Create your models here.
class ClassroomPlans(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type="classroom")


class InstitutionPlans(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type="institution")


class Plan(models.Model):
    options = (("classroom", "Classroom"), ("institution", "Institution"))
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=options)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_active = models.BooleanField(default=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)
    limitations = models.JSONField(null=True, blank=True)

    objects = models.Manager()  # default manager
    classroomPlans = ClassroomPlans()  # custom manager
    institutionPlans = InstitutionPlans()  # custom manager

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ["name", "type"]
