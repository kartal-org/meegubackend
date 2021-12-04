from django.urls import path
from .views_copy import *

urlpatterns = [
    path("", ChatMessageListCreate.as_view()),
    path("", ChatMessageDetail.as_view()),
    path("members/<int:pk>", ChatRoomMemberList.as_view()),
    path("room", ChatRoomList.as_view()),
    path("room/change/<str:code>", ChatRoomDetail.as_view()),
]
