from django.contrib import admin

# Register your models here.
from .models import Chapter, Omen, Tablet


def all_spreadsheets(obj):
    return (', '.join(
        [str(s[1].strip('.xls')) for s in obj.spreadsheet.values_list()]))


def all_tablets(obj):
    return (', '.join([s for s in obj.tablet.values_list()]))


class TabletAdmin(admin.ModelAdmin):
    list_display = ('siglum', 'join', 'ctime', all_spreadsheets)


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('chapter_name', 'ctime')


class OmenAdmin(admin.ModelAdmin):
    list_display = ('omen_id', 'omen_num', 'chapter', all_tablets)


admin.site.register(Omen, OmenAdmin)
admin.site.register(Tablet, TabletAdmin)
admin.site.register(Chapter, ChapterAdmin)
