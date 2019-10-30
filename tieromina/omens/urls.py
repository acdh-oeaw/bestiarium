from django.conf import settings
from django.urls import re_path

from . import views

app_name = 'omens'

urlpatterns = [
    re_path(
        r'^$',
        views.chapters,
        name='chapters',
    ),
    re_path(
        r'^(?P<omenname>({}))$',
        views.omen,
        name='omen',
    ),
]
