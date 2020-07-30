from django.contrib import admin

# Register your models here.
from .models import Sense, SenseTree, Spreadsheet


class SpreadsheetAdmin(admin.ModelAdmin):
    list_display = ('ctime', '__str__', 'user', 'location')


class SenseTreeAdmin(admin.ModelAdmin):
    list_display = ('ctime', 'word_root', 'curated_sense', 'curated_by',
                    'reviewed_by')


class SenseAdmin(admin.ModelAdmin):
    list_display = ('sense_uri', 'sense_tree')


admin.site.register(Spreadsheet, SpreadsheetAdmin)
admin.site.register(SenseTree, SenseTreeAdmin)
admin.site.register(Sense, SenseAdmin)
