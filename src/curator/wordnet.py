import pprint
from collections import Counter, defaultdict
from json import dumps, loads

from networkx import DiGraph
from networkx.readwrite import json_graph
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize


def get_hypernyms(segment_text) -> dict:
    readings = {}
    hypernyms = []
    # collect wordnet senses
    postags = pos_tag(wordpunct_tokenize(segment_text))
    node_parent = {segment_text.upper(): []}
    for text, postag in postags:
        if len(text) < 3: continue
        node_parent = parse_synsets(text, node_parent)

    G = DiGraph()
    print(node_parent)
    for k, v in node_parent.items():
        G.add_node(k)
        for vi in v:
            G.add_node(vi)
            G.add_edge(k, vi)

    json_data = json_graph.node_link_data(G)

    return dumps(json_data, ).replace('"', "\"")


def parse_synsets(word, node_parent):
    hyp = lambda s: s.hypernyms()

    for synset in wordnet.synsets(word):
        node_parent[word.upper()].append(
            synset.name())  # to connect the senses to the root word
        tree = synset.tree(hyp)
        node_parent = parse_tree(tree, synset.name(), node_parent)

    return node_parent


def parse_tree(tree, child, node_tree={}):
    for element in tree:
        if not isinstance(element, list):
            if element.name() == child:
                continue
            else:
                if child in node_tree:
                    if element.name() not in node_tree[child]:
                        node_tree[child].append(element.name())
                else:
                    node_tree[child] = [element.name()]
                child = element.name()
        else:
            parse_tree(element, child, node_tree)
    return node_tree
