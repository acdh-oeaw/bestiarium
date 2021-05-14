from django.urls import re_path

from . import views

app_name = "curator"

urlpatterns = [
    re_path(r"^upload$", views.UploadSpreadSheet.as_view(), name="upload_file"),
    # path(r'loom/<outer>/<inner>', views.loom, name='loom'),
    # path(
    #     r'segments/<chapter>/<page>',
    #     views.view_senses,
    #     name='segments',
    # ),
    # path(
    #     r'segments/<page>/edit/<translation_id>',
    #     views.edit_translation,
    #     name='edit_translation',
    # ),
    # path(
    #     r'sensed3/<word>/',
    #     views.sensed3,
    #     name='sensed3',
    # ),
    # path(
    #     r'segments/<translation_id>/wordsense/<word>/',
    #     views.wordsense,
    #     name='wordsense',
    # ),
    # path(
    #     r'segments/<translation_id>/<word>/save',
    #     views.save_senses,
    #     name='save_senses',
    # ),
    # path(
    #     r'edit-sense/<word>/',
    #     views.edit_sense,
    #     name='edit_sense',
    # ),
    # path(
    #     r'curate-senses',
    #     views.curate_senses,
    #     name='curate_senses',
    # ),
]
