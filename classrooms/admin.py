from django.contrib import admin
from .models import *


class ClassroomConfig(admin.ModelAdmin):
    readonly_fields = ("id",)


admin.site.register(Classroom, ClassroomConfig)
admin.site.register(Resource, ClassroomConfig)
admin.site.register(ClassroomResourceFolder, ClassroomConfig)
admin.site.register(ClassroomResourceQuillFile, ClassroomConfig)
admin.site.register(ClassroomResourceUploadedFile, ClassroomConfig)
admin.site.register(Member, ClassroomConfig)
