from django.db import models
from users.models import NewUser
from workspaces.models import Workspace
from resources.models import InstitutionResource, ClassroomResource
from django.utils import timezone

# Create your models here.


class Note(models.Model):
    title = models.TextField(max_length=50)
    content = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.SET_NULL, null=True, blank=True)
    institutionResource = models.ForeignKey(InstitutionResource, on_delete=models.SET_NULL, null=True, blank=True)
    classroomResource = models.ForeignKey(ClassroomResource, on_delete=models.SET_NULL, null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["owner", "title"]
        ordering = ("-dateUpdated",)

    def __str__(self):
        return self.title
