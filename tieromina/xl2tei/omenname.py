#!/usr/bin/env python
import logging
from collections import namedtuple


class OmenName(namedtuple('OmenName', ['omen_name'])):
    '''
    Creates a namedtuple instance of the omen name
    '''
    omen_name: str  # originally a single string delimited with '.' is passed
    chapter: str
    omen_num: str
    tradition: str = None
    siglum: str = None
    __slots__ = ()

    def __new__(self, omen_name):
        self.omen_name = omen_name
        omen_parts = omen_name.split('.')
        self.chapter = omen_parts[0]
        self.omen_num = omen_parts[-1]
        if len(omen_parts) > 2:
            self.tradition = omen_parts[1]
        if len(omen_parts) > 3:
            self.siglum = omen_parts[2]
        if len(omen_parts) > 4 or len(omen_parts) < 2:
            logging.error(
                'Sheet name %s does not conform '
                'to Chapter.Number or Chapter.Tradition.Number '
                'or Chapter.Tradition.Siglum.Number formats', omen_name)
