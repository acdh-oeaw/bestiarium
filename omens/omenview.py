"""
This acts as an interface between views.py and the model
"""
import logging
import pprint
from collections import Counter, defaultdict

from django.db.models import DecimalField
from django.db.models.functions import Cast

from .models import Chapter, Omen, Translation


def all_chapters() -> dict:
    """
    Returns all the chapters in the database
    TODO: Which order?
    """
    return {"chapters": Chapter.objects.all().order_by("chapter_name")}


def omens_in_chapter(chapter_name: str) -> dict:
    """
    Returns the omens inside a given chapter
    """
    chapter = get_chapter(chapter_name)
    omens = Omen.objects.filter(chapter=chapter)

    message = f"Could not find chapter {chapter_name}" if not chapter else ""

    return {"chapter": chapter, "omens": omens, "error": message}


def witnesses_in_chapter(chapter_name: str) -> dict:
    """
    Returns the witnesses used in a given chapter
    """
    chapter = get_chapter(chapter_name)
    omens = (
        Omen.objects.filter(chapter=chapter)
        .annotate(cast_omen_num=Cast("omen_num", DecimalField()))
        .order_by("cast_omen_num", "omen_num")
    )
    message = f"Cound not find chapter {chapter_name}" if not chapter else ""

    return {"chapter": chapter, "omens": omens, "error": message}


def get_chapter(chapter_name: str) -> Chapter:
    try:
        return Chapter.objects.filter(chapter_name=chapter_name)[0]
    except IndexError:
        logging.error('Could not find chapter "%s"', chapter_name)
        return None


def get_omen(omen_id: str) -> Omen:
    try:
        return Omen.objects.filter(xml_id=omen_id)[0]
    except IndexError:
        logging.error('Could not find omen "%s"', omen_id)
        return None


# def omen_hypernyms(omen_id: str) -> dict:
#     omen = get_omen(omen_id)
#     readings = {}

#     hyp = lambda s: s.hypernyms()

#     for reading in Reconstruction.objects.filter(omen__omen_id=omen.omen_id):
#         readings[reading.reconstruction_id] = {}
#         records = Translation.objects.filter(
#             reconstruction__reconstruction_id=reading.reconstruction_id
#         )

#         for record in records:
#             readings[reading.reconstruction_id][record.translation_id] = {
#                 "safe_id": record.translation_id.replace("_", "-").replace(".", "-"),
#                 "fulltext": record.translation_txt,
#                 "words": [],
#             }
#             # collect wordnet senses
#             postags = nltk.pos_tag(wordpunct_tokenize(record.translation_txt))
#             for text, postag in postags:
#                 sense_info = {"word": text, "senses": []}
#                 for sim in wordnet.synsets(text):
#                     sense_info["senses"].append(
#                         {
#                             "name": sim.name(),
#                             "lemmas": sim.lemma_names(),
#                             "examples": sim.examples(),
#                             "tree": text_viz_hypernyms(sim.tree(hyp)),
#                         }
#                     )

#                 readings[reading.reconstruction_id][record.translation_id][
#                     "words"
#                 ].append(sense_info)

#     return {"data": {"omen": omen, "readings": readings}}


def text_viz_hypernyms(hypernym_tree):
    text = str(hypernym_tree)

    text = text.replace("Synset(", "").replace(")", "").replace("'", "")
    viz_text = ""
    line_pos_len = defaultdict(list)
    line_num = 0
    for word in text.split(","):
        counts = Counter(word)
        word = word.strip().replace("[", "").replace("]", "")
        viz_text += " > " + word if viz_text else word
        line_pos_len[line_num].append(len(word))
        if counts["]"]:
            # viz_text += "\n" + " " * (sum(line_pos_len[line_num][:len(
            #     line_pos_len[line_num]) - counts[']']]) +
            #                           (counts[']'] - 1) * 3)
            words_to_the_left = len(line_pos_len[line_num]) - counts["]"]
            viz_text += "\n" + " " * (
                sum(line_pos_len[0][:words_to_the_left]) + (words_to_the_left - 1) * 3
            )

            line_num += 1
    return pprint.pformat(text).replace("'", "")


def update_translation(translation_id, updated_text):
    db_handle = Translation.objects.get(translation_id=translation_id)
    db_handle.translation_txt = updated_text
    db_handle.save()
    logging.debug("%s - %s", db_handle.translation_id, db_handle.translation_txt)
    return
