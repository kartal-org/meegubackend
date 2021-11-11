from django.contrib import admin
from .models import *


class InstitutionConfig(admin.ModelAdmin):
    readonly_fields = ("id",)


class SubscriptionConfig(admin.ModelAdmin):
    readonly_fields = ("id",)
    list_display = (
        "institution",
        "plan",
        "payerName",
        "payerEmail",
        "paidDate",
    )


admin.site.register(Institution, InstitutionConfig)
admin.site.register(InstitutionSubscription, SubscriptionConfig)
admin.site.register(InstitutionVerification, InstitutionConfig)
admin.site.register(StaffType, InstitutionConfig)
admin.site.register(CustomStaffType, InstitutionConfig)
admin.site.register(Staff, InstitutionConfig)
admin.site.register(InstitutionResource, InstitutionConfig)
