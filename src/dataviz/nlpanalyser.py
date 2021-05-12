"""
This acts as an interface between views.py and the model - performing NLP analysis on the translations
"""
import logging
import pprint
from collections import Counter, defaultdict

import nltk
from django.db.models import DecimalField, IntegerField
from django.db.models.functions import Cast
from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize
from omens.models import Omen, Reconstruction, Segment, Translation

lemmatizer = WordNetLemmatizer()

nltk.download("stopwords")


def wordnet_pos(treebank_tag):
    if treebank_tag.startswith("J"):
        return wordnet.ADJ
    elif treebank_tag.startswith("V"):
        return wordnet.VERB
    elif treebank_tag.startswith("N"):
        return wordnet.NOUN
    elif treebank_tag.startswith("R"):
        return wordnet.ADV

    return None


MORE_STOP_WORDS = ("ditto", "multicolored")
KNOWN_ANIMALS = (
    "gecko",
    "geckos",
    "snake",
    "snakes",
    "lizard",
    "lizards",
    "ant",
    "ants",
    "goat",
    "goats",
    "scorpion",
    "scorpions",
    "ewe",
    "ewes",
    "sheep",
    "sheeps",
    "beetle",
    "beetles",
)


def lemma_pos(segment: str):
    lemmas = defaultdict(list)
    for word, pos in pos_tag(wordpunct_tokenize(segment)):
        if (
            word.lower() in stopwords.words("english")
            or word.lower() in MORE_STOP_WORDS
        ):
            continue

        if word.lower() in KNOWN_ANIMALS:
            pos = "NN"

        wordnet_postag = wordnet_pos(pos)
        if not wordnet_postag:
            continue
        if not word.isalpha():
            continue
        lemma = lemmatizer.lemmatize(
            word.lower(),
            pos=wordnet_postag
            # this leads to gecoks treated as adjectives, and not lemmatized. WTF.
        )
        # print(word, pos, lemmatizer.lemmatize(word.lower(), pos=wordnet_postag))
        # Do not add duplicate words in the segment
        if lemma in MORE_STOP_WORDS:
            continue
        if lemma not in lemmas[wordnet_postag]:
            lemmas[wordnet_postag].append(lemma)

    return lemmas


def complete_translations() -> {}:
    """
    Returns correlation between animals and actions for loom chart
    """
    omens = Omen.objects.all()
    data = []
    for omen in omens:

        # Find reconstructions for the omen
        reconstructions = Reconstruction.objects.filter(
            omen=omen, reconstruction_id__icontains="Copy"
        )
        if not len(reconstructions):
            reconstructions = Reconstruction.objects.filter(
                omen=omen, reconstruction_id__icontains="Var"
            )

        # logging.debug('%s: %s', omen.omen_id, len(reconstructions))
        for r in reconstructions:
            protasis = Translation.objects.filter(
                translation_id__icontains="_protasis", lang="en", reconstruction=r
            )
            apodosis = Translation.objects.filter(
                translation_id__icontains="_apodosis", lang="en", reconstruction=r
            )
            if not (len(protasis) or len(apodosis)):
                # logging.debug(
                #     '%s, %s',
                #     r.reconstruction_id,
                #     "No protasis or apodosis",
                # )
                continue
            protasis_txt = protasis[0].translation_txt.strip()
            apodosis_txt = apodosis[0].translation_txt.strip()

            if not protasis_txt or not apodosis_txt:
                # logging.debug('\n%s: "%s"\n%s: "%s"',
                #               protasis[0].translation_id, protasis_txt,
                #               apodosis[0].translation_id, apodosis_txt)
                continue
            yield {
                "omen": omen.omen_id,
                "protasis": protasis_txt,
                "apodosis": apodosis_txt,
            }


def animals_actions():
    data_counts = defaultdict(int)
    noun_counts = defaultdict(int)
    verb_counts = defaultdict(int)
    postag_data = []
    for t in complete_translations():
        postags = lemma_pos(t["protasis"])
        postag_data.append(postags)
        for noun in postags[wordnet.NOUN]:
            noun_counts[noun] += 1

        for verb in postags[wordnet.VERB]:
            verb_counts[noun] += 1

    sorted_nouns = sorted(noun_counts.items(), key=lambda x: x[1], reverse=True)

    good_nouns = [k[0] for k in sorted_nouns[:10]]

    print(good_nouns)

    for postags in postag_data:
        for noun in postags[wordnet.NOUN]:
            if noun not in KNOWN_ANIMALS:
                continue
            for verb in postags[wordnet.VERB]:
                data_counts[(noun, verb)] += 1
                # print('Apodosis', lemma_pos(t['apodosis']))

    print(data_counts)
    data = []
    for nv_pair, count in data_counts.items():
        if count > 3:
            data.append({"outer": nv_pair[1], "inner": nv_pair[0], "words": count})

    pprint.pprint(data)
    return data


def animals_objects():
    data_counts = defaultdict(int)
    counts_1 = defaultdict(int)
    counts_2 = defaultdict(int)
    postag_data = defaultdict(list)
    for t in complete_translations():
        postags = lemma_pos(t["protasis"])
        postag_data["protasis"].append(postags)
        for noun in postags[wordnet.NOUN]:
            counts_1[noun] += 1

        postags = lemma_pos(t["apodosis"])
        for n2 in postags[wordnet.NOUN]:
            counts_2[noun] += 1

    sorted_nouns = sorted(counts_1.items(), key=lambda x: x[1], reverse=True)

    good_nouns = [k[0] for k in sorted_nouns[:10]]

    print(good_nouns)

    for postags in postag_data:
        for noun in postags[wordnet.NOUN]:
            if noun not in KNOWN_ANIMALS:
                continue
            for verb in postags[wordnet.VERB]:
                data_counts[(noun, verb)] += 1
                # print('Apodosis', lemma_pos(t['apodosis']))

    print(data_counts)
    data = []
    for nv_pair, count in data_counts.items():
        if count > 3:
            data.append({"outer": nv_pair[1], "inner": nv_pair[0], "words": count})

    pprint.pprint(data)
    return data
