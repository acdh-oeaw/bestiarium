from django.conf.urls import url
from django.urls import path, re_path

from . import views

app_name = 'curator'

urlpatterns = [
    re_path(r'^upload$', views.UploadSpreadSheet.as_view(),
            name='upload_file'),
    path(
        r'segments/<page>',
        views.view_senses,
        name='segments',
    ),
    path(
        r'segments/<page>/edit/<translation_id>',
        views.edit_translation,
        name='edit_translation',
    ),
    path(
        r'segments/<page>/<translation_id>/sensed3',
        views.sensed3,
        name='sensed3',
    ),
    path(
        r'segments/<translation_id>/wordsense/<word>/',
        views.wordsense,
        name='wordsense',
    ),
    path(
        r'segments/<translation_id>/<word>/save',
        views.save_senses,
        name='save_senses',
    ),
]
