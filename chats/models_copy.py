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
from django.conf import settings


class ChatRoom(models.Model):

    name = models.CharField(max_length=20)
    members = models.ManyToManyField(
        NewUser, blank=True, help_text="Users who are connected to the chat.", related_name="members"
    )
    admins = models.ManyToManyField(NewUser, blank=True, help_text="Admins of this chat.", related_name="admins")
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def latest_message(self):
        return ChatMessage.objects.filter(room=self.id).values("sender__username", "content").earliest("dateModified")

    class Meta:
        ordering = ("dateModified",)

    # # Hack to pass the user to post save signal.
    # def save(self, *args, **kwargs):
    #     # Hack to pass the user to post save signal.
    #     self.current_authenticated_user = get_current_authenticated_user()
    #     super(ChatRoom, self).save(*args, **kwargs)


class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("dateModified",)

    def __str__(self):
        return self.sender.full_name
