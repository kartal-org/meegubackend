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
            userIds.append(NewUser.objects.get(username=x).id)

        serializer.save(members=userIds)


class ChatRoomDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatRoomSerializer
    queryset = ChatRoom.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatMessageListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatMessageSerializer
    filter_backends = [SearchFilter]
    search_fields = ["room"]
    queryset = ChatMessage.objects.all()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
