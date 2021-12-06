from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsOwner

from rest_framework.permissions import IsAuthenticated

from .models import NewUser
from .utils import Util
from django.urls import reverse

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework.fields import CurrentUserDefault
from django.contrib.sites.shortcuts import get_current_site
import jwt
from django.conf import settings
from django.http import HttpResponsePermanentRedirect
import os

from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter


class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get("APP_SCHEME"), "http", "https"]


class CustomUserCreate(generics.GenericAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_verified=False)
        user_data = serializer.data
        user = NewUser.objects.get(email=user_data["email"])
        token = RefreshToken.for_user(user).access_token

        absurl = "http://" + "localhost:3000/email-verify" + "?token=" + str(token)
        email_body = "Hi " + user.username + " Use the link below to verify your email \n" + absurl
        data = {"email_body": email_body, "to_email": user.email, "email_subject": "Verify your email"}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class ResendActivationLink(generics.GenericAPIView):
    # serializer_class = CustomUserSerializer

    def get(self, request):

        if not request.user.is_verified:
            token = RefreshToken.for_user(request.user).access_token
            absurl = "http://" + "localhost:3000/email-verify" + "?token=" + str(token)
            email_body = "Hi " + request.user.username + " Use the link below to verify your email \n" + absurl
            data = {"email_body": email_body, "to_email": request.user.email, "email_subject": "Verify your email"}
            Util.send_email(data)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)

        # current_site = get_current_site(request)
        # email_subject = 'Activate your account'
        # email_body = render_to_string('authentication/activate.html', {
        #     'user': user,
        #     'domain': absurl,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': token
        # })

        # data = EmailMessage(subject=email_subject, body=email_body,
        #                     from_email=settings.EMAIL_FROM_USER,
        #                     to=[user.email]
        #                     )

        # if not settings.TESTING:
        #     EmailThread(email).start()


class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            user = NewUser.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({"email": "Successfully activated"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get("email", "")

        if NewUser.objects.filter(email=email).exists():
            user = NewUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            # current_site = get_current_site(request=request).domain
            # relativeLink = reverse("password-reset-confirm", kwargs={"uidb64": uidb64, "token": token})

            absurl = "http://localhost:3000/password-reset-confirm?uidb64=" + uidb64 + "&token=" + token
            email_body = "Hello, \n Use link below to reset your password  \n" + absurl
            data = {"email_body": email_body, "to_email": user.email, "email_subject": "Reset your passsword"}
            Util.send_email(data)
        return Response({"success": "We have sent you a link to reset your password"}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get("redirect_url")

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = NewUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url + "?token_valid=False")
                else:
                    return CustomRedirect(os.environ.get("FRONTEND_URL", "") + "?token_valid=False")

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(
                    redirect_url + "?token_valid=True&message=Credentials Valid&uidb64=" + uidb64 + "&token=" + token
                )
            else:
                return CustomRedirect(os.environ.get("FRONTEND_URL", "") + "?token_valid=False")

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url + "?token_valid=False")

            except UnboundLocalError as e:
                return Response(
                    {"error": "Token is not valid, please request a new one"}, status=status.HTTP_400_BAD_REQUEST
                )


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"success": True, "message": "Password reset success"}, status=status.HTTP_200_OK)


class UserRetrieve(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = NewUser.objects.all()
    serializer_class = GetUserSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.request.user.pk)
        return obj


class UserUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    queryset = NewUser.objects.all()
    serializer_class = UserProfileSerializer

    def update(self, request, *args, **kwargs):
        print(request.data)
        return super().update(request, *args, **kwargs)


class UpdateImg(generics.UpdateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    queryset = NewUser.objects.all()
    serializer_class = UserProfileSerializer


class UpdateUserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, format=None):
        print(request.data)
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10


class SearchPeople(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SearchUserSerializer
    queryset = NewUser.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["first_name", "last_name", "username"]
