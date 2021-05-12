from django.conf import settings
from django.urls import path, re_path

from . import views

app_name = 'dataviz'

urlpatterns = [
    re_path(
        'all',
        views.explore,
        name='explore',
    ),
    path(
        'animal-action/',
        views.animal_action,
        name='animal_action',
    ),
    path(
        'animal-objects/',
        views.animal_objects,
        name='animal_objects',
    ),
    path(
        'animal-action-data/',
        views.animal_action_data,
        name='animal_action_data',
    ),
]
