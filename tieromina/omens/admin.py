from django.contrib import admin

# Register your models here.
from .models import Chapter, Omen, Witness


def all_witnesses(obj):
    return (', '.join([s for s in obj.witness.values_list()]))


class WitnessAdmin(admin.ModelAdmin):
    list_display = ('siglum', 'joins', 'ctime')


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('chapter_name', 'ctime')


class OmenAdmin(admin.ModelAdmin):
    list_display = ('omen_id', 'omen_num', 'chapter', all_witnesses)


admin.site.register(Omen, OmenAdmin)
admin.site.register(Witness, WitnessAdmin)
admin.site.register(Chapter, ChapterAdmin)
