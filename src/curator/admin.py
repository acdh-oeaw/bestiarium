from django.contrib import admin

# Register your models here.
from .models import Sense, SenseTree, Upload


class UploadAdmin(admin.ModelAdmin):
    list_display = (
        "ctime",
        "__str__",
        "utype",
        "ustatus",
        "report",
        "user",
        "location",
    )


class SenseTreeAdmin(admin.ModelAdmin):
    list_display = ("ctime", "word_root", "curated_sense", "curated_by", "reviewed_by")


class SenseAdmin(admin.ModelAdmin):
    list_display = ("sense_uri", "sense_tree")


admin.site.register(Upload, UploadAdmin)
admin.site.register(SenseTree, SenseTreeAdmin)
admin.site.register(Sense, SenseAdmin)
