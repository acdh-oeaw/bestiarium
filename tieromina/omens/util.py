'''
Bunch of utility functions shared across the module
'''

import re
from xml.dom import minidom
from xml.etree import ElementTree as ET


def element2string(root):
    '''
    Converts element into an actual string (not bytes!)
    why is this necessary? :sigh:
    '''
    dom = minidom.parseString(ET.tostring(root))
    pretty_root = dom.toprettyxml(indent="", newl="")
    return pretty_root


def pretty_print(root):
    '''
    pretty prints xml elements
    '''
    dom = minidom.parseString(ET.tostring(root))
    pretty_root = dom.toprettyxml(indent="  ", newl="\n")
    print(pretty_root)


def clean_id(dirty_id):
    return re.sub("[^A-Za-z0-9\-_\.]+", "_", dirty_id)
