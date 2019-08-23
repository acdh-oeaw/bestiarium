from django.test import TestCase

from ..omenname import OmenName


class OmenNameTestCase(TestCase):
    def test_simple_omen_name(self):
        omen_name = OmenName('23.11')

    def test_omen_name_with_tradition(self):
        omen_name = OmenName('32.N.1')

    def test_omen_name_with_tradition_and_siglum(self):
        omen_name = OmenName('32.N.K09507(2).4')
