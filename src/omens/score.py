# '''
# Omen score - gathered from different witnesses
# '''
# import logging
# from collections import UserDict, namedtuple
# from typing import List
# from xml.etree import ElementTree as ET

# from xlsx.cell import Cell

# from .lemma import Lemma
# from .line import Line
# from .models import Lemma as LemmaDB
# from .models import Segment as SegmentDB
# from .models import Witness as WitnessDB
# from .namespaces import NS, TEI_NS, XML_ID, get_attribute
# from .position import Position
# from .util import clean_id

# logger = logging.getLogger(__name__)


# class Witness(namedtuple('Witness', 'idno, siglum, joins, reference')):
#     '''
#     A witness - siglum, joins and if applicable, reference
#     '''
#     def __new__(cls, idno, reference):
#         '''
#         Converts the first two column values for a score line into an immutable namedtuple,
#         so it can be used as a key in the score dict
#         '''
#         witness_parts = idno.split('+.')
#         siglum = witness_parts[0]
#         joins = tuple(witness_parts[1:])

#         return super().__new__(cls,
#                                idno=idno,
#                                siglum=siglum,
#                                joins=joins,
#                                reference=reference)

#     @property
#     def xml_id(self):
#         return (f"wit_{clean_id(self.siglum)}_{'_'.join(self.joins)}")

#     @property
#     def unique_id(self):
#         return (
#             f"wit_{clean_id(self.siglum)}_{'_'.join(self.joins)}_{self.reference}"
#         )

#     @property
#     def tei(self):
#         wit = ET.Element(get_attribute('witness', TEI_NS),
#                          {XML_ID: self.xml_id})
#         idno = ET.SubElement(wit, get_attribute('idno', TEI_NS))
#         idno.text = self.idno
#         return wit

#     @property
#     def all_joins(self):
#         return ''.join(['+.' + j for j in self.joins])


# class ScoreLine(Line):
#     '''
#     A line from the score of the omen
#     '''
#     def __init__(self, row: List[Cell], omen_prefix):
#         super().__init__(omen_prefix)
#         idno = ''
#         reference = ''

#         if row[0].column_name == 'A':
#             idno = row[0].full_text
#         else:
#             logger.error('First cell from column A missing: %s', row)
#             raise ValueError(f'col1 must be column A in row: {row}')
#         try:
#             reference = row[1].full_text if row[1].column_name == 'B' else ''
#         except IndexError as ie:
#             pass

#         self.witness = Witness(idno, reference)

#         for cell in row:
#             if not cell.full_text or cell.column_name in 'AB': continue

#             # determine cell type (position - column/line number or lemma)
#             if Position.is_position_cell(cell):  # Position:
#                 position = Position(cell, self.witness)

#                 if position.column: self.data.append(position.column)
#                 self.data.append(position.line)
#             else:
#                 ## Lemma
#                 lemma = Lemma(cell, omen_prefix=self.omen_prefix)
#                 self.data.append(lemma)

#         self.connect_damaged_ends()


# class Score(UserDict):
#     '''
#     A dict of score lines, identified by witness
#     '''
#     def __init__(self, omen_prefix):
#         super().__init__()
#         self.omen_prefix = omen_prefix
#         logging.debug('Score for "%s"', self.omen_prefix)

#     def add_row(self, row: List[Cell]):
#         '''
#         Adds the row to score
#         '''
#         # construct witness
#         scoreline = ScoreLine(row, self.omen_prefix)
#         self.data[scoreline.witness] = scoreline

#     def export_to_tei(self, omen_db):
#         '''
#         returns the TEI representation
#         '''
#         score = ET.Element('div', {'type': 'score'})
#         ab = ET.SubElement(score, 'ab')
#         segment_db = SegmentDB.objects.filter(omen=omen_db,
#                                               segment_type='PROTASIS')[0]
#         for witness, scoreline in self.data.items():
#             wit_db = WitnessDB.objects.get_or_create(witness_id=witness.xml_id,
#                                                      siglum=witness.siglum,
#                                                      joins=witness.all_joins)
#             # omen.witness.add(wit_db)
#             word_idx = 0
#             for item in scoreline:
#                 if isinstance(item, Lemma):
#                     # construct word identifier
#                     # word_id = f'{self.omen_prefix}.{item.xml_id}'
#                     word_node = ab.find(f'.//*[@{XML_ID}="{item.xml_id}"]/app',
#                                         NS)

#                     # This is the correct way to check if the node exists
#                     # if not Node is True even if find returns a match
#                     if word_node is None:
#                         # add new /find corresponding word node
#                         word_parent = ET.Element('w', {XML_ID: item.xml_id})
#                         lemma_db = LemmaDB.objects.get_or_create(
#                             lemma_id=item.xml_id,
#                             lemma_idx=word_idx,
#                             omen=omen_db,
#                             segment=segment_db)
#                         ab.append(word_parent)
#                         word_idx += 1
#                         word_node = ET.SubElement(word_parent, 'app')

#                     # Add lemma to the word node
#                     word_node.append(item.score_tei(witness, self.omen_prefix))
#                 else:  # line/column information
#                     item_tei = item.tei
#                     ab.append(item_tei)

#         return score

#     @property
#     def witnesses(self):
#         '''
#         returns witnesses from the keys
#         '''
#         return list(self.data.keys())
