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
    return re.sub("[^A-Za-z0-9]+", "-", dirty_id)


TEI_TEMPLATE = """
<TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:tei="http://www.tei-c.org/ns/1.0">
  <teiHeader>
      <fileDesc>
         <titleStmt>
            <title>Chapter {{ object.chapter.chapter_name }}</title>
         </titleStmt>
         <publicationStmt>
            <p>born digital</p>
         </publicationStmt>
         <sourceDesc>
            <listWit>{% for x in object.witness.all %}
                <witness xml:id="{{x.xml_id}}">
                    <idno>{{ x.witness_id }}</idno>
                </witness>{% endfor %}
            </listWit>
         </sourceDesc>
      </fileDesc>
  </teiHeader>
  <text>
      <body>
            {{ object.tei_content|safe }}
      </body>
  </text>
</TEI>
"""
