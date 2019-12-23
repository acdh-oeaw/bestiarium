'''
This acts as an interface between views.py and the model
'''
import logging
from collections import Counter, defaultdict

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
    hyp = lambda s: s.hypernyms()

    for reading in Reconstruction.objects.filter(omen__omen_id=omen.omen_id):
        translations[reading.reconstruction_id] = {}
        senses[reading.reconstruction_id] = {}

        records = Translation.objects.filter(
            reconstruction__reconstruction_id=reading.reconstruction_id)
        for record in records:

            if record.segment.segment_id.endswith('P'):
                segment_type = 'PROTASIS'
                translations[reading.reconstruction_id][
                    'fulltext_protasis'] = record.translation_txt
                translations[reading.reconstruction_id][
                    'translation_id_p'] = record.translation_id
            else:
                segment_type = 'APODOSIS'
                translations[reading.reconstruction_id][
                    'fulltext_apodosis'] = record.translation_txt
                translations[reading.reconstruction_id][
                    'translation_id_a'] = record.translation_id

            translations[reading.reconstruction_id][segment_type] = []
            postags = nltk.pos_tag(wordpunct_tokenize(record.translation_txt))
            for text, postag in postags:
                sense_info = {'word': text, 'sense': []}
                for sim in wordnet.synsets(text):
                    sense_info['sense'].append({
                        'name':
                        sim.name(),
                        'lemmas':
                        sim.lemma_names(),
                        'examples':
                        sim.examples(),
                        'tree':
                        text_viz_hypernyms(sim.tree(hyp))
                    })

                translations[reading.reconstruction_id][segment_type].append(
                    sense_info)
    return {'data': {'omen': omen, 'translations': translations}}


def text_viz_hypernyms(hypernym_tree):
    text = str(hypernym_tree)

    text = text.replace('Synset(', '').replace(')', '').replace("'", '')
    # print(text, hypernym_tree)
    viz_text = ''
    line_pos_len = defaultdict(list)
    line_num = 0
    for word in text.split(','):
        counts = Counter(word)
        word = word.strip().replace('[', '').replace(']', '')
        viz_text += ' > ' + word if viz_text else word
        line_pos_len[line_num].append(len(word))
        if counts[']']:
            # viz_text += "\n" + " " * (sum(line_pos_len[line_num][:len(
            #     line_pos_len[line_num]) - counts[']']]) +
            #                           (counts[']'] - 1) * 3)
            words_to_the_left = len(line_pos_len[line_num]) - counts[']']
            viz_text += "\n" + " " * (
                sum(line_pos_len[0][:words_to_the_left]) +
                (words_to_the_left - 1) * 3)

            line_num += 1
    return viz_text


def update_translation(translation_id, updated_text):
    db_handle = Translation.objects.get(translation_id=translation_id)
    db_handle.translation_txt = updated_text
    db_handle.save()
    print(db_handle.translation_id, db_handle.translation_txt)
    return
