from django.contrib import admin
from .models import *

# Register your models here.
class ArticlesConfig(admin.ModelAdmin):
    readonly_fields = ("id",)


admin.site.register(Article, ArticlesConfig)
