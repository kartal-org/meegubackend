from django.db import models
from django.db.models import fields
from rest_framework import serializers
from users.models import NewUser, Profile
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = NewUser
        fields = ("id", "first_name", "last_name", "email", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class GetUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField("get_user_full_name")

    def get_user_full_name(self, obj):
        request = self.context["request"]
        user = request.user
        name = user.first_name + " " + user.last_name
        return name

    class Meta:
        model = NewUser
        fields = (
            "id",
            "name",
            "first_name",
            "last_name",
            "email",
            "username",
            "about",
            "image",
            "cover",
            "is_verified",
        )


class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField("get_user_full_name")

    def get_user_full_name(self, obj):
        request = self.context["request"]
        user = request.user
        name = user.first_name + " " + user.last_name
        return name

    class Meta:
        model = NewUser
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "about",
            "name",
            "email",
            "image",
            "cover",
            "is_verified",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    # password = serializers.CharField(write_only=True, required=True)
    image = serializers.FileField(required=False)
    name = serializers.SerializerMethodField("get_user_full_name")

    def get_user_full_name(self, obj):
        request = self.context["request"]
        user = request.user
        name = user.first_name + " " + user.last_name
        return name

    class Meta:
        model = NewUser
        fields = ("id", "username", "first_name", "last_name", "about", "email", "name", "image", "cover")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    # def validate_password(self, value):
    #     user = self.context["request"].user
    #     if not user.check_password(value):
    #         raise serializers.ValidationError({"password": "Password is not correct"})
    #     return value

    def validate_email(self, value):
        user = self.context["request"].user
        if NewUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context["request"].user
        if NewUser.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.email = validated_data["email"]
        instance.username = validated_data["username"]
        instance.about = validated_data["about"]

        instance.save()

        return instance


class UpdateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ["id", "image"]


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = NewUser
        fields = ["token"]


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ["email"]


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")

            id = force_str(urlsafe_base64_decode(uidb64))
            user = NewUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)

            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise AuthenticationFailed("The reset link is invalid", 401)
        return super().validate(attrs)


class SearchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ["username", "full_name", "image"]
