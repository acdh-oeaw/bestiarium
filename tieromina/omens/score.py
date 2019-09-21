'''
Omen score - gathered from different witnesses
'''
import logging
import re
from collections import UserDict, UserList, namedtuple
from typing import List
from xml.etree import ElementTree as ET

from .cell import Cell
from .lemma import Lemma
from .position import Position

logger = logging.getLogger(__name__)

XML_NS = u'http://www.w3.org/XML/1998/namespace'
NS = {'xml': XML_NS}


class Witness(namedtuple('Witness', 'siglum, joins, reference')):
    '''
    A witness - siglum, joins and if applicable, reference
    '''
    def __new__(cls, row):
        '''
        Converts the first two column values for a score line into an immutable namedtuple,
        so it can be used as a key in the score dict
        '''
        try:
            if row[0].column_name == 'A':
                witness_parts = row[0].full_text.split('+.')
                siglum = witness_parts[0].rstrip('+')
                joins = tuple(witness_parts[1:])
            else:
                logger.error('First cell from column A missing')
                raise ValueError('col1 must be column A')
        except IndexError as ie:
            raise ie

        try:
            reference = row[1].full_text if row[1].column_name == 'B' else ''
        except IndexError as ie:
            reference = ''

        return super().__new__(cls,
                               siglum=siglum,
                               joins=joins,
                               reference=reference)

    @property
    def xml_id(self):
        return "#wit_" + re.sub("[^A-Za-z0-9\-_:\.]+", "_", self.siglum)

    @property
    def tei(self):
        wit = ET.Element('witness', {'xml:id': self.xml_id})
        wit.text = witness.siglum


class ScoreLine(UserList):
    '''
    A line from the score of the omen
    '''
    def __init__(self, row: List[Cell]):
        super().__init__()
        self.witness = Witness(row)
        for cell in row:
            if not cell.full_text or cell.column_name in 'AB': continue

            # determine cell type (position - column/line number or lemma)
            if Position.is_position_cell(cell):  # Position:
                position = Position(cell, self.witness)

                if position.column: self.data.append(position.column)
                self.data.append(position.line)
            else:
                ## Lemma
                lemma = Lemma(cell, self.witness)
                self.data.append(lemma)


class Score(UserDict):
    '''
    A dict of score lines, identified by witness
    '''
    def __init__(self, omen_prefix):
        super().__init__()
        self.omen_prefix = omen_prefix
        logging.debug('Score for "%s"', self.omen_prefix)

    def add_row(self, row: List[Cell]):
        '''
        Adds the row to score
        '''
        # construct witness
        scoreline = ScoreLine(row)
        self.data[scoreline.witness] = scoreline

    @property
    def tei(self):
        '''
        returns the TEI representation
        '''

        score = ET.Element('div', {'type': 'score'})
        ab = ET.SubElement(score, 'ab')
        for witness, scoreline in self.data.items():
            for item in scoreline:
                if isinstance(item, Lemma):
                    # construct word identifier
                    word_id = f'{self.omen_prefix}.{item.xml_id}'
                    id_attrib_name = '{' + XML_NS + '}id'
                    word_node = ab.find(f'.//*[@xml:id="{word_id}"]/app', NS)

                    # This is the correct way to check if the node exists
                    # if not Node is True even if find returns a match
                    if word_node is None:
                        # add new /find corresponding word node
                        word_parent = ET.Element('w',
                                                 {id_attrib_name: word_id})
                        ab.append(word_parent)
                        word_node = ET.SubElement(word_parent, 'app')

                    # Add lemma to the word node
                    lemma_tei = item.tei
                    lemma_tei.attrib['wit'] = witness.xml_id
                    word_node.append(lemma_tei)
                else:  # line/column information
                    item_tei = item.tei
                    ab.append(item_tei)

        return score

    @property
    def witnesses(self):
        '''
        returns witnesses from the keys
        '''
        return list(self.data.keys())
