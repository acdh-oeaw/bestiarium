from django.contrib import admin

from .models import *

# Register your models here.


def all_witnesses(obj):
    return ", ".join([s for s in obj.witness.values_list()])


class WitnessAdmin(admin.ModelAdmin):
    list_display = (
        "witness_id",
        "museum_numbers",
        "provenance",
        "script",
        "state_publication",
        "state_preservation",
        "manuscript_type",
        "tablets_attested",
        "omens_attested",
        "cdli_number",
        "remarks",
        "ctime",
    )


class ChapterAdmin(admin.ModelAdmin):
    list_display = (
        "chapter_name",
        "animal",
        "author",
        "reviewer",
        "proofreader",
        "ctime",
        "introduction"
    )


class OmenAdmin(admin.ModelAdmin):
    list_display = ("xml_id", "omen_name", "omen_num", "chapter", "ctime")


class LemmaAdmin(admin.ModelAdmin):
    list_display = ("xml_id", "lemma_idx", "omen", "segment")


class ReconstructionAdmin(admin.ModelAdmin):
    list_display = ("xml_id", "omen", "label")


class TransliterationAdmin(admin.ModelAdmin):
    list_display = ("xml_id", "reconstruction", "lemma")


class TranscriptionAdmin(admin.ModelAdmin):
    list_display = ("xml_id", "reconstruction", "lemma")


class TranslationAdmin(admin.ModelAdmin):
    list_display = ("xml_id", "segment", "translation_txt", "lang")


class SegmentAdmin(admin.ModelAdmin):
    list_display = ("xml_id", "segment_type", "omen")


class SequenceAdmin(admin.ModelAdmin):
    list_display = ("seq_name", "omen", "position")


admin.site.register(Omen, OmenAdmin)
admin.site.register(Witness, WitnessAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Lemma, LemmaAdmin)
admin.site.register(Reconstruction, ReconstructionAdmin)
admin.site.register(Transliteration, TransliterationAdmin)
admin.site.register(Transcription, TranscriptionAdmin)
admin.site.register(Translation, TranslationAdmin)
admin.site.register(Segment, SegmentAdmin)
