import logging
import os
from json import dumps, loads

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.db import transaction
from django.db.utils import OperationalError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView

from omens.chapter import Chapter
from omens.models import Chapter as ChapterDB
from omens.models import Translation

from .forms import CurateSense, UploadSpreadSheet
from .models import Sense, SenseTree, Spreadsheet
from .wordnet import synset_tree

#from xl2tei.workbook import Workbook

# Create your views here.
UPLOAD_LOC = '/'


def deep_parse(nested_dict, root=False):
    unique_nodes = []
    if not root:
        # add value
        unique_nodes = [nested_dict.get('value')]

    children = []

    if nested_dict.get('children'):
        for child in nested_dict.get('children'):
            unique_nodes.extend(deep_parse(child))

    return list(set(unique_nodes))


@login_required
def save_senses(request, translation_id, word):  #
    dicted = loads(request.body)
    unique_nodes = deep_parse(dicted, root=True)

    trs = Translation.objects.get(translation_id=translation_id)

    # Save sense tree
    try:
        with transaction.atomic():
            try:
                sTree_in_db = SenseTree.objects.get(word=word, translation=trs)
                sTree_in_db.delete()
            except SenseTree.DoesNotExist as dne:
                pass

            sTree = SenseTree.objects.create(word=word,
                                             curated_sense=dumps(dicted),
                                             translation=trs)  # TODO: Add user
            for node in unique_nodes:
                print('Saving', node)
                Sense.objects.create(sense_uri=node, sTree=sTree)

            return HttpResponse("Saved")
    except OperationalError as oe:
        logging.error(repr(oe))
        return HttpResponse("Exception occured")


def wordsense(request, translation_id, word):
    # Check if a Sense Tree exists already
    trs = Translation.objects.get(translation_id=translation_id)
    print(trs, translation_id)
    try:
        stree_from_db = SenseTree.objects.get(word=word, translation=trs)
    except SenseTree.DoesNotExist as dne:
        stree_from_db = SenseTree.objects.filter(word=word).first()

    data = None
    if stree_from_db:
        curated_sense = stree_from_db.curated_sense
        if curated_sense:
            data = loads(curated_sense)

    if not data:
        data = synset_tree(word)

    return JsonResponse(data, safe=False)


def sensed3(request, page, translation_id):
    trs = Translation.objects.get(translation_id=translation_id)
    data = get_hypernyms(trs.translation_txt)
    return JsonResponse(data, safe=False)


@login_required
def view_senses(request, page=1):
    template_name = 'curator/segments.html'
    all_translations = []

    paginator = Paginator(Translation.objects.all(), 4, 1)
    page_obj = paginator.get_page(page)

    # for t in Translation.objects.all():
    #     sense_data = {}
    #     sense_data['translation'] = t
    #     sense_data['hypernyms'] = get_hypernyms(t.translation_txt)
    #     all_translations.append(sense_data)
    # print(len(all_translations))
    # paginator = Paginator(all_translations, 20, 1)
    # page_obj = paginator.get_page(page)
    return render(request, template_name, {
        'page_obj': page_obj,
    })


@login_required
def edit_translation(request, page, translation_id):
    try:
        updated_data = request.GET.dict()
        db_handle = Translation.objects.get(translation_id=translation_id)
        db_handle.translation_txt = updated_data.get(f'input_{translation_id}')
        db_handle.save()
        messages.add_message(request, messages.SUCCESS,
                             'Your changes have been saved!')
    except Exception as e:
        print(repr(e))
        messages.add_message(
            request,
            messages.ERROR,
            'Something went wrong!',
            extra_tags='danger',
        )
        #view_senses(request)
    return redirect(request.META['HTTP_REFERER'])


class CurateSense(LoginRequiredMixin, FormView):
    template_name = 'curator/curate.html'
    omen_id = None
    form_class = CurateSense
    success_url = '.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-1'
        self.helper.field_class = 'col-md-11'
        # self.helper.add_input(Submit('submit', 'save'), )

    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        cd = form.cleaned_data
        #    return render(request, template_name, context)
        return render(self.request, self.template_name, context)


class UploadSpreadSheet(LoginRequiredMixin, FormView):
    template_name = 'upload/upload_spreadsheet.html'
    form_class = UploadSpreadSheet
    success_url = '.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        cd = form.cleaned_data
        uploaded_file = cd.get('upload_file')
        context['filename'] = uploaded_file._name
        with default_storage.open(uploaded_file._name, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        filename = os.path.join(default_storage.location, uploaded_file._name)
        spreadsheet = Spreadsheet(name=uploaded_file._name,
                                  user=self.request.user.username,
                                  location=filename)
        spreadsheet.save()

        try:
            # Add/create a chapter
            chapter = Chapter()
            chapter_db = chapter.export_to_tei(filename)
            # Save upload record
            logging.debug('Default storage: %s', filename)

        except Exception as e:
            context['error'] = repr(e)
            logging.error(repr(e))
            # raise

        return render(self.request, self.template_name, context)
