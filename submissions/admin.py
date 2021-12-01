from django.contrib import admin
from .models import *


class ClassroomConfig(admin.ModelAdmin):
    readonly_fields = ("id",)


admin.site.register(Submission, ClassroomConfig)
admin.site.register(Recommendation, ClassroomConfig)
admin.site.register(SubmissionResponse, ClassroomConfig)
admin.site.register(RecommendationResponse, ClassroomConfig)
# admin.site.register(InstitutionRecommendation)
