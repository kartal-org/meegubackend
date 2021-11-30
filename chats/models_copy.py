from django.db import models
from django.conf import settings
from workspaces.models import Workspace
from classrooms.models import Classroom
from institutions.models import Institution, Department
from users.models import NewUser
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django_currentuser.middleware import get_current_authenticated_user
from django.db.models import F


def defaultPermission():
    return {
        "canDeleteChatRoom": False,
        "canUpdateChatRoom": False,
        "canAddPeople": False,
        "canRemovePeople": False,
    }


class ChatRoom(models.Model):
    name = models.CharField(max_length=20)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.SET_NULL, null=True, blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def members(self):
        return ChatMember.objects.filter(room=self.id).values(
            uid=F("user__id"), first_name=F("user__first_name"), last_name=F("user__last_name")
        )

    class Meta:
        ordering = ("dateModified",)

    # Hack to pass the user to post save signal.
    def save(self, *args, **kwargs):
        # Hack to pass the user to post save signal.
        self.current_authenticated_user = get_current_authenticated_user()
        super(ChatRoom, self).save(*args, **kwargs)


class ChatMember(models.Model):
    options = (
        ("admin", "Admin"),
        ("member", "Member"),
    )
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=options, default="member")

    def __str__(self):
        return self.user.full_name


class ChatMessage(models.Model):
    sender = models.ForeignKey(ChatMember, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("dateModified",)

    def __str__(self):
        return self.sender.user.full_name


# signals
@receiver(post_save, sender=ChatRoom)
def chatroom_create_admin(created, instance, *args, **kwargs):

    if created:
        user = getattr(instance, "current_authenticated_user", None)
        print(user)

        defaultMember = ChatMember.objects.create(room=instance, role="admin", user=user)
        defaultMember.save()
