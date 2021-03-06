from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from django.dispatch import receiver
from django.db.models.signals import post_save  # add this


def upload_to(instance, filename):
    return "userProfile/{filename}".format(filename=filename)


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username, first_name, last_name, password, **other_fields):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, username, first_name, last_name, password, **other_fields)

    def create_user(self, email, username, first_name, last_name, password, **other_fields):

        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    about = models.TextField(_("about"), max_length=500, blank=True)
    profileImage = models.ImageField(
        _("ProfileImage"), upload_to=upload_to, default="userProfile/default_egry2i.jpg", blank=True, null=True
    )
    profileCover = models.ImageField(
        _("ProfileCover"), upload_to=upload_to, default="userProfile/coverDefault_pdrisr.jpg", blank=True, null=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        "Returns the person's full name."
        return "%s %s" % (self.first_name, self.last_name)
