from collections import defaultdict, namedtuple
from enum import Enum
import os, glob, logging, re
from pprint import pprint
from xml.etree import ElementTree as ET
import xml.dom.minidom as minidom
import pandas as pd
import xlrd
from tqdm import tqdm

# from .models import Tablet, Omen

LINE_NUM_COLOR = ((255, 0, 0),)

NAMESPACES =  {'tei': 'http://www.tei-c.org/ns/1.0',
              'xml': 'http://www.w3.org/XML/1998/namespace'}

for namespace, uri in NAMESPACES.items():
    ET.register_namespace(namespace, uri)


class OmenSheet:
    class Witness(namedtuple('Witness', ['siglum', 'ref'])):    
        __slots__ = ()
    
        @property
        def witness_id(self):
            return "wit_" + re.sub("[^A-Za-z0-9\-_:\.]+", "_", self.siglum)
    
    class Reading(namedtuple('Variant', ['varname', 'ref'])):    
        __slots__ = ()
    
        @property
        def variant_id(self):
             return "var_" + re.sub("[^A-Za-z0-9\-_:\.]+", "_", self.siglum)
    

    class ReadingLine:
        '''
        A row containing transliteration, transcription or translation
        '''        
        def __init__(self, row):
            self.row = row
            self.label = row[0].value
            self.ref = row[1].value
            return
        
        @property
        def group_name(self):
            '''
            Removes the trl/trs/en/de part of the label and returns the string
            '''
            p = re.compile(r'^(?P<var_name>\w+)\s*[\((?P<ref_name>.*)\)]*.*\((?P<rdg_type>\w+)\)$')
            m = p.search( self.label)
            group_name = re.sub('\(\w+\)$', '', self.label).strip()
            return  re.sub("[^A-Za-z0-9\-_:\.]+", "_", group_name)
                
        @property
        def row_type(self):
            m = re.match(r'(.*\((?P<rdg_type>\w+)\)$)',  self.label)
            if m:
                return m.group('rdg_type')
            return
        
        
        def __repr__(self):
            return repr(self.row)
            
    class Position:
        '''
        Line, column, obverse and reverse information about the position of the omen in the tablet
        '''
        def __init__(self, cell_value):
            self.cell_value = cell_value        

            self.reverse = 'Reverse' if 'r.' in cell_value else 'Obverse'

            if cell_value and not cell_value.startswith('r') and not cell_value[0].isnumeric() :            
                self.column_break = cell_value.split()[0]
                self.line_break = ' '.join(cell_value.split()[1:])
            else:
                self.line_break = cell_value
                self.column_break = None
            return
        
        
    class Word:
        '''
        A word (in the omen in general, not specific to a reading/witness)
        '''
        def __init__(self, column, omen):
            self.omen = omen
            self.column = column
            return
        
        @property
        def word_id(self):
            return f'{self.omen.lower()}.w.{self.column}'
        
        @property
        def trl_word_id(self):
            return f'{self.omen.lower()}.trl.w.{self.column}'
        
        @property
        def trs_word_id(self):
            return f'{self.omen.lower()}.trs.w.{self.column}'
    
    class Token(Word):
        '''
        Specific reading of a word - either in a score or transliteration or transcription
        '''
        def __init__(self, cell, column, omen):
            self.omen = omen
            self.column = column
            self.cell = cell
            return
        
        def get_token_for_tei(self, div_name='w'):
            tei_div = ET.Element(div_name)
            text_elem = tei_div
            text_elem.text = ''
            to_tail = None
            damage_text = ''
            for i, letter in enumerate(str(self.cell.value)):
                if letter == '[':
                    to_tail = ET.SubElement(tei_div, 'anchor', {'type': 'breakStart'})
                    to_tail.tail = ''
                    # If followed by another letter, create a supplied tag and make that "to_tail"
                    if i+1 < len(str(self.cell.value)) and str(self.cell.value)[i+1].isalpha():
                        text_elem = ET.SubElement(tei_div, 'supplied')                      
                        text_elem.text = ''
                        to_tail = None                        
                elif letter == ']':
                    to_tail = ET.SubElement(tei_div, 'anchor', {'type': 'breakEnd'})
                    to_tail.tail = ''
                elif letter == '.':
                    if i>0:
                        if str(self.cell.value)[i-1] == ' ':
                            damage_text = letter
                        elif str(self.cell.value)[i-1] == '.':
                            damage_text += letter
                            if damage_text == '...':
                                to_tail = ET.SubElement(tei_div, 'gap', {'reason':'damage'})
                                to_tail.tail = ''
                                damage_text = ''
                        elif len(damage_text)<3:
                            continue

                elif damage_text: 
                    if to_tail is not None:
                        to_tail.tail += damage_text
                    else:
                        text_elem.text += damage_text
                    
                    damage_text = ''
                else:
                    if to_tail is not None:
                        to_tail.tail += letter            
                    else:
                        text_elem.text += letter
            return tei_div

        def get_score_reading(self):
            '''
            Reads a token from the score into a rdg tag
            '''
            return self.get_token_for_tei(div_name='rdg')
        
        
    def __init__(self, sheet):
        self.sheet = sheet
        self.score = {}
        self.readings = defaultdict(list)
        self.comment = []
        self.linebreaks = []
        self.read()
        return

    def save_to_db(self, spreadsheet, chapter):
        '''
        Saves the omen into into the database
        
        omen,_ = Omen.objects.get_or_create(omen_num=self.omen_num, spreadsheet=spreadsheet, chapter=chapter)
        for witness in self.score.keys():
            tablet, _ = Tablet.objects.get_or_create(tablet_id=witness.siglum)
            
            omen.tablet.add(tablet)
        return omen
        '''
    
    def read(self):
        self.check_name()
        comment_started = False
        for row_num in range(1, self.sheet.nrows):
            row = self.sheet.row(row_num)
            row_label = row[0].value
            row_ref = row[1].value
            if not row_label and not comment_started:
                if not self.is_empty(row):
                    logging.warning('[Sheet %s] Missing identifier in row %s:\n%s', 
                                    self.sheet.name, row_num, row)

                continue
            elif 'comment' in row_label.lower():
                if comment_started:
                    logging.warning('Unexpected second comments label (%s) in row %s:\n%s', 
                                    row_label, row_num, row)
                comment_started = True
                self.add_to_comments(row)
            elif comment_started:
                self.add_to_comments(row)                
            elif '(' in row_label and ')' in row_label:
                # translation of a known variant
                self.add_to_readings(row)                
            else:
                self.add_to_score(row)
                
            self.linebreaks = sorted(self.linebreaks)
        return
        
    def check_name(self):
        top_cell_val = self.sheet.row(0)[0].value
        if top_cell_val.lstrip('OmenSheet ') != self.sheet.name:
            logging.warning('OmenSheet name in cell A1 (%s) and sheet name (%s) do not match.', 
                            top_cell_val, self.sheet.name)
        self.chapter, self.omen_num = self.sheet.name.split('.')
        self.n = f'OmenSheet {self.chapter}.{self.omen_num}'
        return
    
    def add_to_score(self, row):
        '''
        Score hashed using witness
        '''
        witness = OmenSheet.Witness(siglum=row[0].value, ref=row[1].value)
        self.score[witness] = row
        for i, cell in enumerate(row[2:]):
            col_num = i+2
            if not cell.value or col_num in self.linebreaks:
                continue
                
            cell_format = self.sheet.book.xf_list[cell.xf_index]
            cell_font = self.sheet.book.font_list[cell_format.font_index]
            cell_font_colour = self.sheet.book.colour_map[cell_font.colour_index]
            if (cell_font_colour in LINE_NUM_COLOR and cell_font.italic):
                    self.linebreaks.append(col_num)

        return
    
    def add_to_readings(self, row):
        '''
        Adds rows of readings containing 
        transliterations, transcriptions and translations
        that are NOT marked as "copy text"
        May or may not contain a reference cell (second column)
        Probably corresponds to a "witness" in the score
        '''
        reading = OmenSheet.ReadingLine(row)
        self.readings[reading.group_name].append(reading)           
        return
    
        
    def add_to_comments(self, row):
        '''
        Saves the "label" Philological commentray as the first element in the comment list
        And every subsequent line in the c
        '''
        row_label = row[0].value
        row_ref = row[1].value
        comment_text =  ' '.join([str(cell.value) for cell in row[2:] if str(cell.value).strip()])
        
        if row_ref and not comment_text:
            # in case the comment is entered in the reference column
            comment_text = row_ref
            row_ref = ''
            
        if row_label:
            self.comment.append(row_label)
        
        self.comment.append(comment_text)
            
        return
    
    @staticmethod
    def is_empty(row):
        '''
        returns False if the row or column contains at least one non empty cell
        '''
        for cell in row:
            if cell.value:
                return False
            
        return True
        
    def __repr__(self):
        return f'OmenSheet {self.omen_num} from chapter {self.chapter}'
    
    def get_omen_tei(self):
        '''
        adds a div element for every omen
        '''
        def add_score():
            '''
            Adds Score element with readings (rows)
            '''
            score = ET.SubElement(omen_div, 'div', {'type': 'score'})
            ab = ET.SubElement(score, 'ab')                
            for col in range(2, self.sheet.ncols):
                if self.is_empty(self.sheet.col(col)):
                    continue
                if col not in self.linebreaks:
                    # Open word element
                    word = OmenSheet.Word(col, self.n)
                    w = ET.SubElement(ab, 'w', {'xml:id':word.word_id})
                    app = ET.SubElement(w, 'app')
                for row_num, (witness, row) in enumerate(self.score.items()):
                    if col in self.linebreaks:
                        # Mark linebreak
                        pos = OmenSheet.Position(str(row[col].value))
                        if pos.column_break:
                            cb = ET.SubElement(ab, 'cb', {'n':pos.column_break,
                                                     'ed': f'#{witness.witness_id}'})
                            if witness.ref:
                                cb.attrib['corresp'] = witness.ref

                        if pos.line_break:
                            lb = ET.SubElement(ab, 'lb', {'n':pos.line_break,
                                                     'ed': f'#{witness.witness_id}'})
                            if witness.ref:
                                lb.attrib['corresp'] = witness.ref

                    elif row[col].value: 
                        token = OmenSheet.Token(row[col], col, self.n)
                        rdg = token.get_score_reading()
                        rdg.attrib['wit'] = f'#{witness.witness_id}'
                        rdg.attrib['xml:id'] = f'omen{self.chapter}.{self.omen_num}.w.{col}.rdg{row_num}'
                        if witness.ref:
                            rdg.attrib['corresp'] = witness.ref
                        app.append(rdg)
            return
        
        def add_comments():
            '''
            Adds philological commentary            
            '''
            comment_div = ET.SubElement(omen_div, 'div', {'type': 'commentary'})
            head = ET.SubElement(comment_div, 'head')
            head.text = self.comment[0]
            for comment in self.comment[1:]:
                p = ET.SubElement(comment_div, 'p')
                p.text = comment
            return
        
        def add_readings():
            '''
            Adds readings - transliterations, transcriptions and translations
            '''
            def add_transliteration():
                '''
                
                '''
                reading_div.attrib['type'] = 'transliteration'
                if reading.ref:
                    reading_div.attrib['corresp'] = reading.ref

                for i, cell in enumerate(reading.row[2:]):
                    col_num = i + 2
                    if cell.value:
                        word = OmenSheet.Token(cell, col_num, self.n)
                        w = word.get_token_for_tei()
                        w.attrib['xml:id'] = word.trl_word_id
                        w.attrib['corresp'] = f'#{word.word_id}'
                        reading_div.append(w)

                return
            
            def add_transcription():
                '''
                Adds transcription
                '''
                reading_div.attrib['type'] = 'transcription'
                if reading.ref:
                    reading_div.attrib['corresp'] = reading.ref

                for i, cell in enumerate(reading.row[2:]):
                    col_num = i + 2
                    if cell.value:
                        word = OmenSheet.Token(cell, col_num, self.n)
                        w = word.get_token_for_tei()

                        w.attrib['xml:id']=word.trs_word_id
                        w.attrib['corresp'] = f'#{word.trl_word_id}'
                        reading_div.append(w)

                return

            def add_translation():
                '''
                adds translation
                '''
                if reading.ref:
                    reading_div.attrib['corresp'] = reading.ref
                reading_div.attrib['type'] = 'translation'
                reading_div.attrib['lang'] = reading.row_type
                reading_div.text = ' '.join([str(cell.value) for cell in reading.row[2:] if str(cell.value).strip()])
                return
            
            for group_name, readings in self.readings.items():
                group_type = 'copyText' if group_name.lower().startswith('copy') else 'variant'
                readings_div = ET.SubElement(omen_div, 'div', {'type': group_type, 
                                                               'n': group_name})
                for reading in readings:
                    reading_div = ET.SubElement(readings_div, 'ab', {'type':reading.row_type})                    
                    if reading.row_type == 'trl':
                        add_transliteration()
                    elif reading.row_type == 'trs':
                        add_transcription()
                    else:
                        add_translation()                        
            return
        
        omen_div = ET.Element('div', {'n': self.n})
        omen_head = ET.SubElement(omen_div, 'head')
        omen_head.text = self.n
        add_score()
        add_readings()
        add_comments()
        return omen_div
