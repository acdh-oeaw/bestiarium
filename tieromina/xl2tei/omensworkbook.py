from collections import defaultdict, namedtuple
from enum import Enum
import os, glob, logging, re
from xml.etree import ElementTree as ET
import xml.dom.minidom as minidom
import pandas as pd
import xlrd
from tqdm import  tqdm
from .omen import Omen

TEI_BASE_LOC = '/mnt/acdh_resources/tieromina'

def pretty_print(root):
    '''
    pretty prints xml elements
    '''
    dom = minidom.parseString(ET.tostring(root))
    pretty_root = dom.toprettyxml(indent="  ", newl="\n")
    return pretty_root


NAMESPACES =  {'tei': 'http://www.tei-c.org/ns/1.0',
              'xml': 'http://www.w3.org/XML/1998/namespace'}

for namespace, uri in NAMESPACES.items():
    ET.register_namespace(namespace, uri)


class OmensWorkbook:
    def __init__(self, wbfile):
        self.wbfile = wbfile
        self.book = xlrd.open_workbook(wbfile, formatting_info=True)
        self.omens ={}
        self.witnesses = {}
        self.chapter = None
        for sheet in self.book.sheets():
            omen = Omen(sheet)
            self.omens[sheet.name] = omen
            if not self.chapter: self.chapter = omen.chapter
        return
       
    def export_to_tei(self, tei_base_loc=TEI_BASE_LOC, overwrite=False):
        '''       
        Omens are read one by one from the sheets,
        and are encoded to TEI with relevant headers
        '''
        title_added = False

        def add_omen_witnesses():
            '''
            One witness for one sigla
            Alternate readings from the same sigla are mentioned in resp
            '''
            
            listwit = root.find('./teiHeader/sourceDesc/listWit', NAMESPACES)
            

            for witness in omen.score.keys():
                if witness.witness_id not in self.witnesses.keys():
                    self.witnesses[witness.witness_id] = witness.siglum
                    wit = ET.SubElement(listwit, 'witness', {'xml:id': witness.witness_id})
                    wit.text = witness.siglum
        
            return
        
        def add_resp_text():
            '''
            When a new source is added, resp is correspondingly updated
            '''
            pass
        
        def add_title():
            '''
            when reading the first omen from file, 
            the title is added to the header
            '''
            title_text = f'Chapter {omen.chapter}'
            self.chapter = omen.chapter
            title_tag = root.find('./teiHeader/fileDesc/titleStmt/title', NAMESPACES)
            body_tag = root.find('./text/body/head', NAMESPACES)
            title_tag.text = title_text
            body_tag.text = title_text
            title_added = True
            return
        
        def add_outline():
            '''
            adds the TEI skeleton
            '''
            header = ET.SubElement(root, 'teiHeader')
            fileDesc = ET.SubElement(header, 'fileDesc')
            titleStmt = ET.SubElement(fileDesc, 'titleStmt')
            title = ET.SubElement(titleStmt, 'title')  
            editor = ET.SubElement(titleStmt, 'editor')  
            respStmt = ET.SubElement(titleStmt, 'respStmt')  
            publicationStmt = ET.SubElement(fileDesc, 'publicationStmt')
            p = ET.SubElement(publicationStmt, 'p')
            p.text = 'Working copy, for internal use only'
            sourceDesc = ET.SubElement(header, 'sourceDesc')
            ET.SubElement(sourceDesc, 'listWit')
            
            text = ET.SubElement(root, 'text')
            body = ET.SubElement(text, 'body')
            ET.SubElement(body, 'head')
            
            return
        
           
        # Start creating TEI for the set of omens
        # check if a TEI already exists for the given chapter
        
        out_file = os.path.join(tei_base_loc, f'chapter_{self.chapter}.xml')
        if os.path.exists(out_file):
            root = ET.parse(out_file).getroot()
            title_added = True
        else:           
            root = ET.Element('TEI')            
            add_outline()

        body = root.find('.//text/body', NAMESPACES)

        for omen_name, omen in self.omens.items():
            # if the chapter title hasn't been added, add it
            if not title_added:
                add_title()

            existing_omen_div =  root.find(f".//text/body/div[@n='{omen.n}']")
            if  existing_omen_div and not overwrite:
                logging.warning('Omen already present, Skipping. Rerun with "overwrite" flag set if needed.')
                continue
            if overwrite and existing_omen_div:
                # removes existing omen div so it can be added again
                body.remove(existing_omen_div)
                
            add_omen_witnesses()
            omen_div = omen.get_omen_tei()
            # delete and add div, if omen already present
            body.append(omen_div)
        # save TEI

        logging.debug(pretty_print(root))

        with open(out_file, 'w') as f:
            f.write(ET.tostring(root, encoding='unicode'))
            logging.info('Saved to %s', out_file)
        return
