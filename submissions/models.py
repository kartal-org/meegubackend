from django.db import models
from workspaces.models import Workspace, WorkspaceFile, Member
from institutions.models import Institution
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
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)
    adviserResponse = models.CharField(max_length=10, choices=options, default="pending")
    institutionResponse = models.CharField(max_length=10, choices=institutionOptions, default="pending")
    status = models.CharField(max_length=10, choices=status_options, default="draft")
    comment = models.TextField(null=True, blank=True)
    isSend = models.BooleanField(default=False)
    # workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, null=True, blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True)
    file = models.ForeignKey(
        WorkspaceFile, on_delete=models.RESTRICT, related_name="submission_files", null=True, blank=True
    )

    class Meta:

        ordering = ["-dateUpdated"]

    def __str__(self):
        return self.title

    @property
    def authors(self):

        workspace = self.file.folder.workspace.id

        return Member.objects.filter(workspace=workspace).values(
            uid=F("user__id"), first_name=F("user__first_name"), last_name=F("user__last_name")
        )


# class ClassroomSubmission(Submission):
#     workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)


# class InstitutionRecommendation(Submission):
#     submission = models.ForeignKey(ClassroomSubmission, on_delete=models.CASCADE)
#     institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
