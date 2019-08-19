from ..wbformat import WBFormat
from unittest.mock import patch, call, ANY, PropertyMock, MagicMock
from django.test import TestCase
import xlrd

class WorkbookFormatTestCase(TestCase):
    
    def setUp(self):
        self.wbfmt = WBFormat(xf_list=[1,2,3],
                              font_list=['a', 'b', 'c'])

