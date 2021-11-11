from django.contrib import admin
from .models import *

# Register your models here.
class ModelConfig(admin.ModelAdmin):
    readonly_fields = ("id",)


admin.site.register(Workspace, ModelConfig)
admin.site.register(Member, ModelConfig)
admin.site.register(WorkspaceFolder, ModelConfig)
admin.site.register(WorkspaceQuillFile, ModelConfig)
admin.site.register(WorkspaceUploadedFile, ModelConfig)
