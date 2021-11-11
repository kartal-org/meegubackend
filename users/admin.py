from django.contrib import admin
from users.models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ("email", "username", "first_name", "last_name")
    list_filter = ("email", "username", "first_name", "last_name", "is_active", "is_staff")
    ordering = ("-start_date",)
    list_display = ("id", "email", "username", "first_name", "last_name", "is_active", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "username", "first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_verified",
                )
            },
        ),
        (
            "Personal",
            {
                "fields": (
                    "about",
                    "image",
                    "cover",
                )
            },
        ),
    )
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 20, "cols": 60})},
    }
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "first_name", "password1", "password2", "is_active", "is_staff"),
            },
        ),
    )


admin.site.register(NewUser, UserAdminConfig)

admin.site.register(Profile)
