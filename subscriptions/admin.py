from django.contrib import admin
from .models import *

# Register your models here.
class Config(admin.ModelAdmin):
    readonly_fields = ("id",)


admin.site.register(Plan, Config)
admin.site.register(ClassroomSubscription, Config)
admin.site.register(InstitutionSubscription, Config)
