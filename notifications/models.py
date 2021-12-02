from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from institutions.models import InstitutionVerification
from users.models import NewUser


class Notification(models.Model):
    class UnreadNofif(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(isRead=False)

    options = (("verification", "verification"), ("submission", "submission"), ("invitation", "invitation"))
    type = models.CharField(choices=options, max_length=20)
    receiver = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="+",
    )
    message = models.TextField(null=True, blank=True)
    isRead = models.BooleanField(default=False)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    unread = UnreadNofif()

    class Meta:
        ordering = ["-dateModified"]

    def __str__(self) -> str:
        return "%s  (%s)" % (self.sender.username, self.dateModified)


# @receiver(post_save, sender=InstitutionVerification)
# def apply_verification_handler(created, instance, *args, **kwargs):
#     if created:  # if a verification is created
#         notif = Notification.objects.create(sender=instance.institution.owner, type="verification")

#         notif.receiver.add(NewUser.objects.get(pk=1).id)
#         notif.save()
#     if instance.status == "approved":
#         notif = Notification.objects.create(
#             sender=NewUser.objects.get(pk=1),
#             type="verification",
#             message="Your verification application is accepted!",
#         )

#         notif.receiver.add(instance.institution.owner)
#         notif.save()
#     if instance.status == "disapproved":
#         notif = Notification.objects.create(
#             sender=NewUser.objects.get(pk=1),
#             type="verification",
#             message="Your verification application is disapproved!",
#         )

#         notif.receiver.add(instance.institution.owner)
#         notif.save()
