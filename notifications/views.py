from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *

# Create your views here.
class NotificationList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # members__in=[self.request.user]
        return Notification.objects.filter(receiver__in=[self.request.user])


class NotificationModify(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
