from django.test import TestCase

from ..omenname import OmenName


class OmenNameTestCase(TestCase):
    def test_simple_omen_name(self):
        omen_name = OmenName('23.11'.split('.'))
        return

    def test_omen_name_with_tradition(self, mock_sheet_name):
        omen_name = OmenName('32.N.1'.split('.'))
        return

    def test_omen_name_with_tradition_and_siglum(self, mock_sheet_name):
        omen_name = OmenName('32.N.K09507(2).4'.split('.'))
        return
