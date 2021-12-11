from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from institutions.models import InstitutionVerification
from submissions.models import *
from users.models import NewUser
from .pusher import pusher_client


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
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+", blank=True, null=True
    )
    message = models.TextField(null=True, blank=True)
    isRead = models.BooleanField(default=False)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)
    redirectID = models.IntegerField(null=True, blank=True)

    objects = models.Manager()
    unread = UnreadNofif()

    class Meta:
        ordering = ["-dateModified"]

    def __str__(self) -> str:
        return "%s  (%s)" % (self.sender.username, self.dateModified)


@receiver(post_save, sender=InstitutionVerification)
def apply_verification_handler(created, instance, *args, **kwargs):
    # if created:  # if a verification is created
    #     notif = Notification.objects.create(sender=instance.institution.owner, type="verification")

    #     notif.receiver.add(NewUser.objects.get(pk=1).id)
    #     notif.save()
    print(instance.status)
    if instance.status == "approved":

        pusher_client.trigger(
            "notification",
            instance.institution.creator.username,
            {
                "type": "verification",
                "message": "%s verification application is disapproved!" % instance.institution.name,
                "redirectID": instance.institution.id,
                # "room": self.request.data["room"],
            },
        )
        notif = Notification.objects.create(
            sender=NewUser.objects.get(pk=1),
            type="verification",
            message="%s verification application is disapproved!" % instance.institution.name,
            redirectID=instance.institution.id,
        )

        notif.receiver.add(instance.institution.creator)
        notif.save()
    if instance.status == "disapproved":

        pusher_client.trigger(
            "notification",
            instance.institution.creator.username,
            {
                "type": "verification",
                "message": "%s verification application is disapproved!" % instance.institution.name,
                "redirectID": instance.institution.id,
                # "room": self.request.data["room"],
            },
        )
        notif = Notification.objects.create(
            sender=NewUser.objects.get(pk=1),
            type="verification",
            message="%s verification application is disapproved!" % instance.institution.name,
            redirectID=instance.institution.id,
        )

        notif.receiver.add(instance.institution.creator)
        notif.save()


@receiver(post_save, sender=Submission)
def submission_create_handler(created, instance, *args, **kwargs):
    if created:
        # breakpoint()
        pusher_client.trigger(
            "notification",
            instance.file.folder.workspace.classroom.adviserInstance.username,
            {
                "type": "submission",
                "message": "A submission is created at %s" % instance.file.folder.workspace.classroom.name,
                "redirectID": instance.file.folder.workspace.classroom.id,
                # "room": self.request.data["room"],
            },
        )
        notif = Notification.objects.create(
            # sender=NewUser.objects.get(pk=1),
            type="verification",
            message="A submission is created at %s" % instance.file.folder.workspace.classroom.name,
            redirectID=instance.file.folder.workspace.classroom.id,
        )
        # adviserInstance
        notif.receiver.add(instance.file.folder.workspace.classroom.adviserInstance)
        notif.save()
        pass
