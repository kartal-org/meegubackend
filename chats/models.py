from django.db import models
from django.conf import settings


class Conversation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    # user = models.CharField(max_length=2)
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver", blank=True, null=True
    )
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ("timestamp",)


class PublicChatRoom(models.Model):
    title = models.CharField(max_length=255, blank=False)
    # code = models.CharField(max_length=12, unique=True, blank=False)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, help_text="Users who are connected to the chat.", related_name="users"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        return self.title

    def connect_user(self, user):
        is_user_added = False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added = True
        elif user in self.users.all():
            is_user_added = True
        return is_user_added

    def disconnect_user(self, user):
        """
        return true if user is remove in the list
        """
        is_user_removed = False
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True
        return is_user_removed

    @property
    def group_name(self):
        return "PublicChatRoom-" + self.id


class PublicRoomChatMessageManager(models.Manager):
    def by_room(self, room):
        qs = PublicRoomChatMessage.object.filter(room=room).order_by("-timestamp")
        return qs


class PublicRoomChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(PublicChatRoom, on_delete=models.CASCADE, related_name="messages")
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique=False, blank=False)

    objects = PublicRoomChatMessageManager()

    class Meta:
        ordering = ("timestamp",)

    def __str__(self):
        return "%s: %s" % (self.user, self.content)
