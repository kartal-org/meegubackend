from django.db import models

# from institutions.models import Department
from workspaces.models import Workspace, WorkspaceFile, Member

# from institutions.models import Institution
from django.db.models import F


# Create your models here.
class Submission(models.Model):
    options = (("accepted", "Accepted"), ("revise", "Revise"), ("rejected", "Rejected"), ("pending", "Pending"))
    institutionOptions = (
        ("accepted", "Accepted"),
        ("revise", "Revise"),
        ("rejected", "Rejected"),
        ("pending", "Pending"),
        ("published", "Published"),
    )
    status_options = (("draft", "Draft"), ("submit", "Submit"))

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    file = models.ForeignKey(
        WorkspaceFile, on_delete=models.RESTRICT, related_name="submission_files", null=True, blank=True
    )
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=status_options, default="draft")

    class Meta:

        ordering = ["-dateUpdated"]

    def __str__(self):
        return "%s - (%s)" % (self.title, self.file.folder.workspace.name)

    @property
    def authors(self):

        workspace = self.file.folder.workspace.id

        return Member.objects.filter(workspace=workspace).values(
            uid=F("user__id"), first_name=F("user__first_name"), last_name=F("user__last_name")
        )


class Recommendation(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    department = models.ForeignKey("institutions.Department", on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - (%s)" % (self.submission.title, self.submission.file.folder.workspace.name)


class Response(models.Model):
    options = (("accepted", "Accepted"), ("revise", "Revise"), ("rejected", "Rejected"), ("pending", "Pending"))
    responseStatus = models.CharField(choices=options, max_length=20)
    comment = models.TextField(null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ClassroomSubmissionResponse(Response):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - (%s)" % (self.submission.title, self.dateModified)


class InstitutionRecommendationResponse(Response):
    options = (
        ("accepted", "Accepted"),
        ("revise", "Revise"),
        ("rejected", "Rejected"),
        ("pending", "Pending"),
        ("published", "Published"),
    )
    responseStatus = models.CharField(choices=options, max_length=20)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
