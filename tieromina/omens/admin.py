from django.contrib import admin

# Register your models here.
from .models import Chapter, Tablet


def all_spreadsheets(obj):
    return (', '.join(
        [str(s[1].strip('.xls')) for s in obj.spreadsheet.values_list()]))


class TabletAdmin(admin.ModelAdmin):
    list_display = ('siglum', 'join', 'ctime', all_spreadsheets)


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('chapter_name', 'ctime')


admin.site.register(Tablet, TabletAdmin)
admin.site.register(Chapter, ChapterAdmin)
