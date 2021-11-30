from django.contrib import admin
from .models import *


class ClassroomConfig(admin.ModelAdmin):
    readonly_fields = ("id",)


admin.site.register(Submission, ClassroomConfig)
admin.site.register(Recommendation, ClassroomConfig)
admin.site.register(ClassroomSubmissionResponse, ClassroomConfig)
admin.site.register(InstitutionRecommendationResponse, ClassroomConfig)
# admin.site.register(InstitutionRecommendation)
