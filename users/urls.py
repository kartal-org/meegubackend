from django.urls import path
from .views import *

app_name = "users"

urlpatterns = [
    path("register/", CustomUserCreate.as_view(), name="register"),
    path("email-verify/", VerifyEmail.as_view(), name="verify-email"),
    path("me/", UserRetrieve.as_view(), name="retrieve_user"),
    # path("profile/", UpdateUserProfileView.as_view(), name="retrieve_userProfile"),
    path("profile/<int:user>", GetUserProfileView.as_view(), name="retrieve_userProfile"),
    path("me/edit/<int:pk>/", UserUpdateDestroy.as_view(), name="retrieve_user"),
    path("request-reset-email/", RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path("password-reset-confirm/<uidb64>/<token>/", PasswordTokenCheckAPI.as_view(), name="password-reset-confirm"),
    path("password-reset-complete", SetNewPasswordAPIView.as_view(), name="password-reset-complete"),
    # Search and Filters
    path("search", SearchPeople.as_view(), name="search_user"),
]
