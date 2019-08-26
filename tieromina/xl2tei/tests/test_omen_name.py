from django.test import TestCase

from ..omenname import OmenName


class OmenNameTestCase(TestCase):
    def test_simple_omen_name(self):
        omen_name = OmenName('23.11')
        self.assertEqual(omen_name.omen_name, '23.11')
        self.assertEqual(omen_name.chapter, '23')
        self.assertEqual(omen_name.omen_num, '11')
        self.assertIsNone(omen_name.tradition)
        self.assertIsNone(omen_name.siglum)

    def test_omen_name_with_tradition(self):
        omen_name = OmenName('32.N.1')
        self.assertEqual(omen_name.omen_num, '1')
        self.assertEqual(omen_name.tradition, 'N')
        self.assertEqual(omen_name.chapter, '32')

    def test_omen_name_with_tradition_and_siglum(self):
        omen_name = OmenName('32.N.K09507(2).4')
        self.assertEqual(omen_name.omen_num, '4')
        self.assertEqual(omen_name.siglum, 'K09507(2)')
        self.assertEqual(omen_name.tradition, 'N')
        self.assertEqual(omen_name.chapter, '32')
