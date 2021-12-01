from django.db import models
from django.db.models.fields import CharField
from django.conf import settings


def defaultPermission():
    return {
        "canDeleteProduct": False,
        "canUpdateProduct": False,
        "canAddPeople": False,
        "canRemovePeople": False,
        "canCreateResources": False,
        "canDeleteResources": False,
        "canUpdateResources": False,
    }


# Base model for all members
class BaseMember(models.Model):
    options = (("approved", "Approved"), ("pending", "Pending"), ("rejected", "Rejected"))
    status = models.CharField(max_length=10, choices=options, default="approved")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    def __str__(self):
        return self.user.full_name

    class Meta:
        abstract = True


class BaseMemberType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    permissions = models.JSONField(default=defaultPermission)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
