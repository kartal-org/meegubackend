from django.db import models
from users.models import NewUser
from django.utils import timezone

# Create your models here.


class Note(models.Model):
    title = models.TextField(max_length=50)
    content = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(NewUser, related_name="notes_owner", on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(default=timezone.now)
    dateUpdated = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ["owner", "title"]
        ordering = ("-dateUpdated",)

    def __str__(self):
        return self.title
