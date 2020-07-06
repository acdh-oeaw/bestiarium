from django.contrib import admin

# Register your models here.
from .models import SenseTree, Spreadsheet


class SpreadsheetAdmin(admin.ModelAdmin):
    list_display = ('ctime', '__str__', 'user', 'location')


class SenseTreeAdmin(admin.ModelAdmin):
    list_display = ('ctime', '__str__', 'curated_sense', 'segment',
                    'curated_by', 'reviewed_by')


admin.site.register(Spreadsheet, SpreadsheetAdmin)
admin.site.register(SenseTree, SenseTreeAdmin)
