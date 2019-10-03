'''
Represents the reconstructions of an omen
'''
import logging
import re
from collections import UserDict, UserList, defaultdict
from typing import NamedTuple
from xml.etree import ElementTree as ET

from .lemma import Lemma
from .line import Line

logger = logging.getLogger(__name__)


class ReconstructionId(NamedTuple):
    '''
    Hashable identifier for a readling line
    '''
    label: str
    siglum: str = ''


class ReconstructionLine(Line):
    '''
    A list of lemmas that make a reconstruction line
    '''
    reconstruction_type: str

    def __init__(self, row: list, omen_prefix):
        super().__init__(omen_prefix)
        m = re.match(
            r'^(?P<label>[a-zA-Z\s]*)\s(?P<siglum>.*)\((?P<rdg_type>[a-zA-Z]*)\)$',
            row[0].full_text)
        if not m: raise ValueError('Unrecognised row header %s', row)
        self.reconstruction_id = ReconstructionId(
            label=m.group('label'), siglum=m.group('siglum'))

        self.rdg_type = m.group('rdg_type')
        for cell in row:
            if not cell.full_text or cell.column_name in 'AB': continue
            self.data.append(Lemma(cell, omen_prefix=self.omen_prefix))

        self.connect_damaged_ends()

    def export_to_tei(self, reconstruction_db):
        ab = ET.Element('ab')
        if self.rdg_type == 'trl':
            ab.attrib['type'] = 'transliteration'
        elif self.rdg_type == 'trs':
            ab.attrib['type'] = 'transcription'
        else:
            ab.attrib['type'] = 'translation'
            ab.attrib['lang'] = self.rdg_type

        if self.rdg_type in ('trl', 'trs'):
            for word in self.data:
                w = word.reconstruction_tei(self.omen_prefix)
                ab.append(w)

        else:  # No W tag in translations - but it contains text, might contain anchor elements for breaks
            for i, word in enumerate(self.data):
                if i == 0:
                    w = word.reconstruction_tei(self.omen_prefix)
                    w.tag = 'ab'
                    ab = w
                    ab.attrib['lang'] = self.rdg_type
                    ab.attrib['type'] = 'translation'
                    if 'corresp' in ab.attrib:
                        del ab.attrib['corresp']

                else:
                    ab.text += ' ' + w.text
                    logger.warning(
                        'Unexpected values in translation row; expecting only one cell, \n%s',
                        word)

        return ab


class Reconstruction(UserDict):
    '''
    Keys are ReconstructionId
    Comprises of reconstructions which could be one or more of the following:
     - transliteration,
     - transcription,
     - translation
    '''

    def __init__(self, omen_prefix):
        super().__init__()
        self.omen_prefix = omen_prefix
        self.data = defaultdict(list)

    def add_to_reconstruction(self, row: list):
        '''
        Identifies the score line and adds it to the score
        '''
        reconstruction_line = ReconstructionLine(row, self.omen_prefix)
        self.data[reconstruction_line.reconstruction_id].append(
            reconstruction_line)

    def export_to_tei(self, omen_db):
        for rdg_grp, lines in self.data.items():
            elem = ET.Element('div', {'n': rdg_grp.label})
            for line in lines:
                elem.append(line.export_to_tei(omen_db))
            yield elem
