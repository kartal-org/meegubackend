from django.contrib import admin
from .models import *

# Register your models here.
class LibraryItemConfig(admin.ModelAdmin):
    readonly_fields = ("id",)


admin.site.register(LibraryItem, LibraryItemConfig)
