from collections import defaultdict

import nltk
import numpy as np
import pandas as pd
import spacy
from django.shortcuts import render
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, wordpunct_tokenize

# Create your views here.
from .models import Chapter, Omen, Reconstruction, Translation
from .omenview import all_chapters, get_chapter, omens_in_chapter

wordnet_lemmatizer = WordNetLemmatizer()
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


def chapters(request):
    template_name = 'omens/chapters.html'
    context = all_chapters()
    return render(request, template_name, context)


def chapter_detail(request, chapter_name):
    template_name = 'omens/chapter_detail.html'
    context = omens_in_chapter(chapter_name)
    return render(request, template_name, context)


def chapter_tei(request, chapter_name):
    template_name = 'omens/tei.xml'
    chapter = get_chapter(chapter_name=chapter_name)
    context = {'tei': chapter.tei}
    return render(request, template_name, context, content_type='text/xml')


def omen_detail(request, omen_id):
    template_name = 'omens/omen_detail.html'
    omen = Omen.objects.filter(omen_id=omen_id)[0]
    translations = {}
    senses = {}
    for reading in Reconstruction.objects.filter(omen__omen_id=omen.omen_id):
        print(reading)
        translations[reading.reconstruction_id] = {}
        senses[reading.reconstruction_id] = {}

        records = Translation.objects.filter(
            reconstruction__reconstruction_id=reading.reconstruction_id)
        for record in records:
            if record.segment.segment_id.endswith('P'):
                segment_type = 'PROTASIS'
            else:
                segment_type = 'APODOSIS'

            translations[reading.reconstruction_id][segment_type] = []
            postags = nltk.pos_tag(wordpunct_tokenize(record.translation_txt))
            print(postags)
            for text, postag in postags:
                sense_info = {'word': text, 'sense': []}
                for sim in wordnet.synsets(text):
                    print(text, sim.name(), sim.lemma_names())
                    sense_info['sense'].append({
                        'name': sim.hypernyms(),
                        'lemmas': sim.lemma_names(),
                        'examples': sim.examples()
                    })

                translations[reading.reconstruction_id][segment_type].append(
                    sense_info)

    print(translations)
    context = {'data': {'omen': omen, 'translations': translations}}
    return render(request, template_name, context, content_type='text/html')


def omen_tei(request, omen_id):
    template_name = 'omens/tei.xml'
    omen = Omen.objects.filter(omen_id=omen_id)[0]
    context = {'tei': omen.tei}
    return render(request, template_name, context, content_type='text/xml')
