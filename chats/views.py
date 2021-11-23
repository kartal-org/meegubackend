from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, filters, generics, permissions, status
from .pusher import pusher_client
from .models import *
from .serializers import *
import shortuuid
from users.models import NewUser
from rest_framework.parsers import JSONParser


def get_code():
    codeID = shortuuid.ShortUUID().random(length=8)
    return codeID


class MessageAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessagesSerializer

    def perform_create(self, serializer):
        user = self.request.user
        message = self.request.data["message"]
        receiver = NewUser.objects.get(id=self.request.data["receiver"])
        pusher_client.trigger(
            "chat",
            "message",
            {
                "user": self.request.user.username,
                "message": self.request.data["message"],
                "receiver": self.request.data["receiver"],
            },
        )

        print(self.request.user)
        serializer.save(user=user, message=message, receiver=receiver)
        return Response([])

    # def post(self, request, *args, **kwargs):
    #     user = request.data["user"]
    #     message = request.data["message"]
    #     pusher_client.trigger(
    #         "chat",
    #         "message",
    #         {
    #             "user": request.data["user"],
    #             "message": request.data["message"],
    #         },
    #     )
    #     print(message, user)

    #     return Response([])


class GetMessagesAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessagesSerializer

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(user=user)


# ChatRoom
class CreateMessageRoomView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreatePublicChatRoomSerializer
    parser_classes = [JSONParser]

    def perform_create(self, serializer):

        # receiver username
        receiver = self.request.data["receiver"]
        receiverInstance = NewUser.objects.get(username=receiver)
        receiverID = receiverInstance.id
        users = [self.request.user, receiverID]
        derivedTitle = receiverInstance.first_name + " " + receiverInstance.last_name
        print(receiverID)

        serializer.save(users=users, title=derivedTitle)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        receiver = request.data["receiver"]
        receiverInstance = NewUser.objects.get(username=receiver)
        receiverID = receiverInstance.id
        users = [self.request.user.id, receiverID]
        derivedTitle = receiverInstance.first_name + " " + receiverInstance.last_name
        payload = {"id": serializer.data, "users": users, "title": derivedTitle}
        print(receiverID)

        return Response(payload, status=status.HTTP_201_CREATED, headers=headers)


class GetMessageRoomView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PublicChatRoomSerializer

    def get_queryset(self):
        user = self.request.user
        return PublicChatRoom.objects.filter(users__in=[user])


class SendMessageView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SendPublicRoomChatMessageSerializer

    def perform_create(self, serializer):

        room = PublicChatRoom.objects.get(id=self.request.data["room"])
        roomChannel = "publicChat-%d" % (self.request.data["room"])
        content = self.request.data["content"]
        user = self.request.user
        pusher_client.trigger(
            roomChannel,
            "message",
            {
                "user": self.request.user.username,
                "content": self.request.data["content"],
                "room": self.request.data["room"],
            },
        )
        serializer.save(user=user, content=content, room=room)
        return Response([])


class GetMessagesView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PublicRoomChatMessageSerializer

    def get_queryset(self):
        room = self.kwargs.get("pk")
        return PublicRoomChatMessage.objects.filter(room=room)
