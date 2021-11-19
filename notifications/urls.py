from django.urls import path

from .views import *

urlpatterns = [
    path("", NotificationList.as_view(), name="notification_list"),
    path("change/<int:pk>", NotificationModify.as_view(), name="notification_detail"),
]
