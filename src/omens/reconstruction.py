'''
Represents the reconstructions of an omen
'''
import logging
import re
from collections import UserDict, UserList, defaultdict, namedtuple
from typing import NamedTuple
from xml.etree import ElementTree as ET

from .lemma import Lemma
from .line import Line
from .models import Lemma as LemmaDB
from .models import Reconstruction as ReconstructionDB
from .models import Segment as SegmentDB
from .models import Transcription as TranscriptionDB
from .models import Translation as TranslationDB
from .models import Transliteration as TranslitDB
from .namespaces import XML_ID
from .util import clean_id

logger = logging.getLogger(__name__)


class ReconstructionId(
        namedtuple('ReconstructionId', 'omen_prefix,label,witness')):
    @classmethod
    def idno_parts(cls, idno):
        m = re.match(
            r'^(?P<label>[a-zA-Z\s]*)\s(?P<siglum>.*)\((?P<rdg_type>[a-zA-Z]*)\)$',
            idno)
        if not m: raise ValueError('Unrecognised row header %s', row)
        return namedtuple('idno', 'label,witness,rdg_type')(
            label=m.group('label'),
            witness=m.group('siglum')[1:-1],
            rdg_type=m.group('rdg_type'))

    def __new__(cls, omen_prefix, idno):
        '''
        Converts the first two column values for a score line into an immutable namedtuple,
        so it can be used as a key in the score dict
        '''
        ip = ReconstructionId.idno_parts(idno)
        return super().__new__(cls,
                               omen_prefix=omen_prefix,
                               label=ip.label,
                               witness=ip.witness)

    @property
    def xml_id(self):
        return (self.omen_prefix + '.' + clean_id(self.label) +
                ('.' + clean_id(self.witness) if self.witness else ''))


class ReconstructionLine(Line):
    '''
    A list of lemmas that make a reconstruction line
    The information about Apodosis is obtained in one of these lines - and updated
    '''
    reconstruction_type: str

    def __init__(self, row: list, omen_prefix):
        super().__init__(omen_prefix)
        self.reconstruction_id = ReconstructionId(
            omen_prefix=omen_prefix,
            idno=row[0].full_text,
        )
        ip = ReconstructionId.idno_parts(idno=row[0].full_text)
        self.rdg_type = ip.rdg_type
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
                if word.apodosis:
                    logging.debug('Reconstruction; found apodosis @ %s',
                                  word.xml_id)
                    try:
                        lemma_db = LemmaDB.objects.get(lemma_id=word.xml_id)
                        lemma_db.set_segment_type_to_apodosis()

                    except Exception as e:
                        logging.debug('Could not change %s to APODOSIS',
                                      word.xml_id)

                w = word.reconstruction_tei(self.omen_prefix)
                ab.append(w)

        else:  # No W tag in translations - but it contains text, might contain anchor elements for breaks
            full_translation = ''
            for i, word in enumerate(self.data):
                full_translation += ' ' + word.plain_text
                if i > 0:
                    logger.warning(
                        'Unexpected values in translation row; expecting only one cell, \n%s',
                        word)

            translation_parts = full_translation.split('–')
            if len(translation_parts) == 1:
                translation_parts.append('')
            elif len(translation_parts) > 2:
                translation_parts[1] = '-'.join(translation_parts[1:])

            logging.debug('PARTS: %s', translation_parts)

            protasis_element = ET.Element(
                'div',
                {
                    XML_ID: self.xml_id + '_protasis',
                    'type': 'protasis'
                },
            )
            protasis_element.text = translation_parts[0]
            ab.append(protasis_element)

            protasis_translation_db = TranslationDB(
                translation_id=self.xml_id + '_protasis',
                reconstruction=reconstruction_db,
                segment=SegmentDB.protasis(reconstruction_db.omen),
                translation_txt=translation_parts[0].replace('[', '').replace(
                    ']', ''))
            protasis_translation_db.save()

            apodosis_element = ET.Element('div', {
                XML_ID: self.xml_id + '_apodosis',
                'type': 'apodosis'
            })
            apodosis_element.text = translation_parts[1]
            ab.append(apodosis_element)

            apodosis_translation_db = TranslationDB(
                translation_id=self.xml_id + '_apodosis',
                reconstruction=reconstruction_db,
                segment=SegmentDB.apodosis(reconstruction_db.omen),
                translation_txt=translation_parts[1].replace('[', '').replace(
                    ']', ''))

            apodosis_translation_db.save()

            # w = word.reconstruction_tei(self.omen_prefix)
            # w.tag = 'ab'
            # w.attrib = ab.attrib
            # ab = w

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
            recon_db = ReconstructionDB(reconstruction_id=clean_id(
                rdg_grp.xml_id),
                                        label=rdg_grp.label,
                                        omen=omen_db)
            recon_db.save()
            for line in lines:
                elem.append(line.export_to_tei(recon_db))

            yield elem
