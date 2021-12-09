from django.db import models
from files.models import *
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum


def upload_to(instance, filename):
    return "classroom/{filename}".format(filename=filename)


# Create your models here.
class ClassroomResource(Package):
    classroom = models.ForeignKey("classrooms.Classroom", on_delete=models.CASCADE)
    institution = models.ForeignKey("institutions.Institution", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = (
            "classroom",
            "name",
        )

    @property
    def storageUsed(self):
        return ClassroomResourceFile.objects.filter(folder__resource=self).aggregate(Sum("size"))["size__sum"]


class ClassroomResourceFolder(Folder):
    resource = models.ForeignKey(ClassroomResource, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["name", "resource"]


class ClassroomResourceFile(File):
    folder = models.ForeignKey(
        ClassroomResourceFolder,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    class Meta:
        unique_together = ["name", "folder"]


class InstitutionResource(Package):
    # institution = models.ForeignKey("institutions.Institution", on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey("institutions.Department", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = (
            "name",
            "department",
        )


class InstitutionResourceFolder(Folder):
    resource = models.ForeignKey(InstitutionResource, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["name", "resource"]


class InstitutionResourceFile(File):
    folder = models.ForeignKey(
        InstitutionResourceFolder,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    class Meta:
        unique_together = ["name", "folder"]
