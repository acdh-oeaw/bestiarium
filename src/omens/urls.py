from django.conf import settings
from django.urls import path, re_path

from . import views

app_name = 'omens'

urlpatterns = [
    re_path(
        r'^chapters$',
        views.chapters,
        name='chapters',
    ),
    path(
        'chapters/<chapter_name>',
        views.chapter_detail,
        name='chapter_detail',
    ),
    path(
        'chapters/<chapter_name>/tei',
        views.chapter_tei,
        name='chapter_tei',
    ),
    path(
        'chapters/<chapter_name>/tei.xml',
        views.chapter_tei_raw,
        name='chapter_tei_raw',
    ),
    path(
        'chapters/<chapter_name>/tei2html',
        views.chapter_xsl,
        name='chapter_xsl',
    ),
    path(
        '<omen_id>',
        views.omen_detail,
        name='omen_detail',
    ),
    path(
        '<omen_id>/tei2html',
        views.omen_xsl,
        name='omen_xsl',
    ),
    path(
        '<omen_id>/tei',
        views.omen_tei,
        name='omen_tei',
    ),
    path(
        '<omen_id>/tei.xml',
        views.omen_tei_raw,
        name='omen_tei',
    ),
    path(
        '<omen_id>/edit/<translation_id>',
        views.edit_translation,
        name='edit_translation',
    ),
]
