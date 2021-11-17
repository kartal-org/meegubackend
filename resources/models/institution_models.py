from django.db import models
from files.models import *
from django.utils.translation import gettext_lazy as _


class InstitutionResource(Package):
    institution = models.ForeignKey("institutions.Institution", on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey("institutions.Department", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = (
            "name",
            "institution",
        )


class InstitutionResourceFolder(Folder):
    resource = models.ForeignKey(InstitutionResource, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["name", "resource"]


class InstitutionResourceQuillFile(QuillFile):
    folder = models.ForeignKey(
        InstitutionResourceFolder,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    class Meta:
        unique_together = ["name", "folder"]


class InstitutionResourceUploadedFile(UploadedFile):
    folder = models.ForeignKey(
        InstitutionResourceFolder,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
