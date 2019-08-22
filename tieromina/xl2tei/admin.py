
from django.contrib import admin

# Register your models here.
from .models import (Chapter, Commentary, Omen, Reference, Tablet, Token,
                     Transcription, Translation, Transliteration)


def all_spreadsheets(obj):
    return (', '.join([str(s[1].strip('.xls')) for s in obj.spreadsheet.values_list()]))


class TabletAdmin(admin.ModelAdmin):
    list_display = ('siglum', 'join', 'ctime', all_spreadsheets)


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('chapter_id', 'ctime')



admin.site.register(Tablet, TabletAdmin)
admin.site.register(Reference)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Omen)

admin.site.register(Token)

admin.site.register(Transliteration)
admin.site.register(Transcription)

admin.site.register(Translation)
admin.site.register(Commentary)
