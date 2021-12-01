from django.db import models
from django.conf import settings
from posts.models import Publication


class LibraryItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "publication"]

    def __str__(self):
        return self.publication.title
