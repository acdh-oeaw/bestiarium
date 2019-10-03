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
from .models import Reconstruction as ReconstructionDB
from .namespaces import XML_ID
from .util import clean_id

logger = logging.getLogger(__name__)


class ReconstructionId(NamedTuple):
    '''
    Hashable identifier for a readling line
    '''
    omen_prefix: str
    label: str
    siglum: str = ''

    @property
    def xml_id(self):
        return (self.omen_prefix + '.' + clean_id(self.label) +
                ('.' + clean_id(self.siglum) if self.siglum else ''))


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
            omen_prefix=omen_prefix,
            label=m.group('label'),
            siglum=m.group('siglum')[1:-1])

        self.rdg_type = m.group('rdg_type')
        self.reference = row[1].full_text if row[1].column_name == 'B' else ''
        for cell in row:
            if not cell.full_text or cell.column_name in 'AB': continue
            self.data.append(Lemma(cell, omen_prefix=self.omen_prefix))

        self.connect_damaged_ends()

    @property
    def xml_id(self):
        return f'{self.rdg_type}.{self.reconstruction_id.xml_id}{"_"+clean_id(self.reference) if self.reference else ""}'

    def export_to_tei(self, reconstruction_db):
        ab = ET.Element('ab', {XML_ID: self.xml_id})
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
                    w.attrib = ab.attrib
                    ab = w
                else:
                    ab.text += ' ' + w.text
                    logger.warning(
                        'Unexpected values in translation row; expecting only one cell, \n%s',
                        word)

        return ab


class Reconstruction(UserDict):
    '''
    Keys are ReconstructionIdb
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
            elem = ET.Element('div', {
                'n': rdg_grp.label,
                XML_ID: clean_id(rdg_grp.xml_id)
            })
            # Create a database record for this reconstruction
            recon_db = ReconstructionDB(
                reconstruction_id=clean_id(rdg_grp.xml_id), omen=omen_db)
            recon_db.save()
            for line in lines:
                elem.append(line.export_to_tei(recon_db))
            yield elem
