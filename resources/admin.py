from django.contrib import admin
from .models import *


class ResourceConfig(admin.ModelAdmin):
    readonly_fields = ("id",)


admin.site.register(ClassroomResource, ResourceConfig)
admin.site.register(ClassroomResourceFolder, ResourceConfig)
admin.site.register(ClassroomResourceFile, ResourceConfig)
admin.site.register(InstitutionResource, ResourceConfig)
admin.site.register(InstitutionResourceFolder, ResourceConfig)
admin.site.register(InstitutionResourceFile, ResourceConfig)
