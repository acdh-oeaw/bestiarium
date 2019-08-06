from django.contrib import admin

# Register your models here.
from .models import Spreadsheet


class SpreadsheetAdmin(admin.ModelAdmin):
    list_display = ('ctime', '__str__')

admin.site.register(Spreadsheet, SpreadsheetAdmin)
