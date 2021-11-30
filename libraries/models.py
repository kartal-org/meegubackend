from django.db import models
from django.conf import settings
from posts.models import Publication

# Create your models here.


# class Library(models.Model):
#     owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

#     def __str__(self):
#         return "%s %s's Library" % (self.owner.first_name, self.owner.last_name)


class LibraryItem(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    content = models.ForeignKey(Publication, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["owner", "content"]

    def __str__(self):
        return self.content.title
