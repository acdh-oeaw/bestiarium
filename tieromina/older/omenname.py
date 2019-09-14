#!/usr/bin/env python

import logging
from collections import namedtuple


class OmenName(
        namedtuple(
            'OmenName',
            ['omen_name', 'chapter', 'omen_num', 'tradition', 'siglum'])):
    '''
    Creates a namedtuple instance of the omen name
    '''
    omen_name: str  # originally a single string delimited with '.' is passed
    chapter: str
    omen_num: str
    tradition: str
    siglum: str
    __slots__ = ()

    def __new__(cls, omen_name):
        omen_name = omen_name
        omen_parts = omen_name.split('.')
        chapter = omen_parts[0]
        omen_num = omen_parts[-1]
        tradition = omen_parts[1] if len(omen_parts) > 2 else None

        siglum = omen_parts[2] if len(omen_parts) > 3 else None
        if len(omen_parts) > 4 or len(omen_parts) < 2:
            logging.error('Sheet name %s does not conform '
                          'to Chapter.Number or Chapter.Tradition.Number '
                          'or Chapter.Tradition.Siglum.Number formats',
                          omen_name)

        cls._inst = super().__new__(cls, omen_name, chapter, omen_num,
                                    tradition, siglum)
        return cls._inst
