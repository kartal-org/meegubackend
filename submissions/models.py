from django.db import models
from workspaces.models import Workspace, WorkspaceQuillFile, WorkspaceUploadedFile
from institutions.models import Institution


# Create your models here.
class Submission(models.Model):
    options = (("accepted", "Accepted"), ("revise", "Revise"), ("rejected", "Rejected"))
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=options)
    comment = models.TextField(null=True, blank=True)
    isSend = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ["-dateUpdated"]

    def __str__(self):
        return self.title


class ClassroomSubmission(Submission):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    file = models.ManyToManyField(WorkspaceQuillFile, related_name="temporary_submission_files")
    uploadfile = models.ManyToManyField(WorkspaceUploadedFile, related_name="submission_files")


class InstitutionRecommendation(Submission):
    submission = models.ForeignKey(ClassroomSubmission, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
