from django.db import models
from files.models import *
from django.utils.translation import gettext_lazy as _
from classrooms.models import Classroom


def upload_to(instance, filename):
    return "classroom/{filename}".format(filename=filename)


# Create your models here.
class ClassroomResource(Package):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    institution = models.ForeignKey("institutions.Institution", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = (
            "classroom",
            "name",
        )


class ClassroomResourceFolder(Folder):
    resource = models.ForeignKey(ClassroomResource, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["name", "resource"]


class ClassroomResourceQuillFile(QuillFile):
    folder = models.ForeignKey(
        ClassroomResourceFolder,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    class Meta:
        unique_together = ["name", "folder"]


class ClassroomResourceUploadedFile(UploadedFile):
    folder = models.ForeignKey(
        ClassroomResourceFolder,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    class Meta:
        unique_together = ["name", "folder"]
