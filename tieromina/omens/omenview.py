'''
This acts as an interface between views.py and the model
'''
import logging

import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize

from .models import Chapter, Omen, Reconstruction, Translation

wordnet_lemmatizer = WordNetLemmatizer()
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


def all_chapters() -> dict:
    '''
    Returns all the chapters in the database
    TODO: Which order?
    '''
    all_chapters = Chapter.objects.all()
    return {'chapters': all_chapters}


def omens_in_chapter(chapter_name: str) -> dict:
    '''
    Returns the omens inside a given chapter
    '''
    chapter = get_chapter(chapter_name)
    omens = Omen.objects.order_by('omen_num').filter(chapter=chapter)
    message = f'Cound not find chapter {chapter_name}' if not chapter else ''
    return {'chapter': chapter, 'omens': omens, 'error': message}


def get_chapter(chapter_name: str) -> Chapter:
    try:
        return Chapter.objects.filter(chapter_name=chapter_name)[0]
    except IndexError:
        logging.error('Could not find chapter "%s"', chapter_name)
        return None


def get_omen(omen_id: str) -> Omen:
    try:
        return Omen.objects.filter(omen_id=omen_id)[0]
    except IndexError:
        logging.error('Could not find omen "%s"', omen_id)
        return None


def omen_hypernyms(omen_id: str) -> dict:
    omen = get_omen(omen_id)
    translations = {}
    senses = {}
    for reading in Reconstruction.objects.filter(omen__omen_id=omen.omen_id):
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
    return {'data': {'omen': omen, 'translations': translations}}
