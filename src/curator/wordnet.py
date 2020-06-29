import pprint
from collections import Counter, defaultdict
from json import dumps, loads

from networkx import DiGraph
from networkx.readwrite import json_graph
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize


def synset_tree(word):
    hyper = lambda s: s.hypernyms()
    node_id = 0
    G = DiGraph()
    G.add_node(node_id, value=word)
    for s in wordnet.synsets(word):
        tree = s.tree(hyper)
        print(tree)
        G, node_id = parse_synset_tree(tree, G, node_id, 0)
    return json_graph.tree_data(G, root=0)


def parse_synset_tree(nested_tree, G, node_id, parent_node):
    for item in nested_tree:
        if isinstance(item, list):
            G, node_id = parse_synset_tree(item, G, node_id, parent_node)
        else:
            G.add_node(node_id + 1,
                       value=item.name(),
                       pos=item.pos(),
                       defn=item.definition(),
                       examples=item.examples())
            G.add_edge(parent_node, node_id + 1)
            node_id += 1
            parent_node = node_id

    return G, node_id
