from django.contrib import admin

# Register your models here.
from .models import (Chapter, Lemma, Omen, Reconstruction, Segment,
                     Transcription, Translation, Transliteration, Witness)


def all_witnesses(obj):
    return (', '.join([s for s in obj.witness.values_list()]))


class WitnessAdmin(admin.ModelAdmin):
    list_display = ('siglum', 'joins', 'ctime')


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('chapter_name', 'ctime')


class OmenAdmin(admin.ModelAdmin):
    list_display = ('omen_id', 'omen_num', 'chapter', all_witnesses)


class LemmaAdmin(admin.ModelAdmin):
    list_display = ('lemma_id', 'lemma_idx', 'omen', 'segment')


class ReconstructionAdmin(admin.ModelAdmin):
    list_display = ('reconstruction_id', 'omen')


class TransliterationAdmin(admin.ModelAdmin):
    list_display = ('trl_id', 'reconstruction', 'lemma')


class TranscriptionAdmin(admin.ModelAdmin):
    list_display = ('trs_id', 'reconstruction', 'lemma')


class TranslationAdmin(admin.ModelAdmin):
    list_display = ('translation_id', 'segment', 'translation_txt')


class SegmentAdmin(admin.ModelAdmin):
    list_display = ('segment_id', 'segment_type', 'omen')


admin.site.register(Omen, OmenAdmin)
admin.site.register(Witness, WitnessAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Lemma, LemmaAdmin)
admin.site.register(Reconstruction, ReconstructionAdmin)
admin.site.register(Transliteration, TransliterationAdmin)
admin.site.register(Transcription, TranscriptionAdmin)
admin.site.register(Translation, TranslationAdmin)
admin.site.register(Segment, SegmentAdmin)
