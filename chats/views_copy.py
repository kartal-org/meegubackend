from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from .pusher import pusher_client
from .models_copy import *
from .serializers_copy import *
import shortuuid
from users.models import NewUser
from rest_framework.parsers import JSONParser
from rest_framework.filters import SearchFilter, OrderingFilter
from .pusher import pusher_client


class ChatRoomList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        return ChatRoom.objects.filter(members__in=[self.request.user])

    def perform_create(self, serializer):
        userData = self.request.data.get("members")

        userIds = []
        for x in userData:
            print(x)
            # breakpoint()
            userIds.append(NewUser.objects.get(username=x).id)

        serializer.save(members=userIds)


class ChatRoomMemberList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatRoomGetMembersSerializer
    queryset = ChatRoom.objects.all()

    # def get_queryset(self):
    #     return ChatRoom.objects.filter(members__in=[self.request.user])


class ChatRoomDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatRoomSerializer
    # queryset = ChatRoom.objects.all()
    lookup_field = "code"

    def get_queryset(self):
        # breakpoint()
        return ChatRoom.objects.filter(code=self.kwargs.get("code"))

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatMessageListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatMessageSerializer
    filter_backends = [SearchFilter]
    search_fields = ["room__code"]
    queryset = ChatMessage.objects.all()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        roomChannel = self.request.data["room"]
        # send sender data other than id
        pusher_client.trigger(
            "chat",
            roomChannel,
            {
                "sender": {
                    "id": self.request.user.id,
                    "username": self.request.user.username,
                    "full_name": self.request.user.full_name,
                    "profileImage": self.request.user.profileImage.url,
                },
                "content": self.request.data["content"],
                "room": self.request.data["room"],
            },
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ChatMessageDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatMessageSerializer
    filter_backends = [SearchFilter]
    search_fields = ["room__id"]
    queryset = ChatMessage.objects.all()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
