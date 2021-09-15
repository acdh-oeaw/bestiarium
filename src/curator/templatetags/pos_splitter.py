from django import template
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.tokenize import wordpunct_tokenize

register = template.Library()

STOP_WORDS = ('the', 'man', 'and', 'will', 'onto', 'them', 'they', 'thereby',
              'all', 'that', 'his', 'are', 'each', 'who', 'him', 'out', 'onto',
              'ditto', 'take', 'into', 'then', 'from', 'but', 'its', 'for')


@register.filter(name='tokens')
def tokens(value):
    """
        Returns tokens for sense analysis
    """
    postags = pos_tag(dict.fromkeys(wordpunct_tokenize(value)))
    relevant_tokens = []
    for w, pos in postags:
        if w.isalpha() and len(w) > 2 and w not in STOP_WORDS:
            # relevant_tokens.append((w, pos))
            if wordnet.synsets(w):
                yield ((w, pos))

    return


@register.filter(name='goodwords')
def good_words(all_words):
    """
        Returns a filtered list of candidate words for senses
    """
    relevant_tokens = []
    for w in all_words:
        wclean = w.replace('[', '').replace(']', '')
        if wclean.isalpha() and len(wclean) > 2 and wclean not in STOP_WORDS:
            if wordnet.synsets(wclean):
                yield (w, wclean, all_words.get(w))

    return
