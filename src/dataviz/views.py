from django.http import JsonResponse
from django.shortcuts import render

from .nlpanalyser import *


# Create your views here.
def explore(request):
    template_name = 'dataviz/explore.html'
    context = {}
    return render(request, template_name, context)


def animal_action(request):
    template_name = 'dataviz/animal_action.html'
    context = {'dataviz_title': 'Animals and their actions'}
    return render(request, template_name, context)


def animal_objects(request):
    context = {'dataviz_title': 'Animals and Nouns in Apodosis'}
    template_name = 'dataviz/animal_objects.html'

    return render(request, template_name, context)


def animal_objects_data(request):
    return JsonResponse(animals_actions(), safe=False)


def animal_action_data(request):
    return JsonResponse(animals_actions(), safe=False)
