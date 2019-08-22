from django.test import TestCase

from ..tablet import Tablet

class TabletTestCase(TestCase):
    def setUp(self):        
        pass

    def test_tablet_without_joins(self):
        tablet = Tablet('VAT 10805')
        self.assertEqual(tablet.siglum, 'VAT 10805')
        self.assertEqual(tablet.joins, None)
        return


    def test_tablet_with_physical_joins(self):
        tablet = Tablet('SU 51/49+')
        self.assertEqual(tablet.siglum, 'SU 51/49')
        self.assertEqual(tablet.joins, [''])
        return

    def test_tablet_with_one_non_physical_join(self):
        tablet = Tablet('VAT 10481+.1')
        self.assertEqual(tablet.siglum, 'VAT 10481')
        self.assertEqual(tablet.joins, ['.1'])
        return

    def test_tablet_with_multiple_non_physical_joins(self):
        # TODO: Find a real example for this
        tablet = Tablet('VAT 10481+.1+.2')
        self.assertEqual(tablet.siglum, 'VAT 10481')
        self.assertEqual(tablet.joins, ['.1', '.2'])
        return

