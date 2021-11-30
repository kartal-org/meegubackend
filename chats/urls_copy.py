from django.urls import path
from .views_copy import *

urlpatterns = [
    path("", ChatMessageListCreate.as_view()),
    path("room", ChatRoomList.as_view()),
    path("room/change/<int:pk>", ChatRoomDetail.as_view()),
]
