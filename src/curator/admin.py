from django.contrib import admin

# Register your models here.
from .models import Spreadsheet, WordSenses


class SpreadsheetAdmin(admin.ModelAdmin):
    list_display = ('ctime', '__str__', 'user', 'location')


class WordSensesAdmin(admin.ModelAdmin):
    list_display = ('ctime', '__str__', 'curated_sense', 'segment',
                    'curated_by', 'reviewed_by')


admin.site.register(Spreadsheet, SpreadsheetAdmin)
admin.site.register(WordSenses, WordSensesAdmin)
