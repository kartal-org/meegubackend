from django.contrib import admin
from .models import *


class ClassroomConfig(admin.ModelAdmin):
    readonly_fields = ("id",)


admin.site.register(Classroom, ClassroomConfig)
admin.site.register(ClassroomMember, ClassroomConfig)

# admin.site.register(ClassroomSubscription, ClassroomConfig)
