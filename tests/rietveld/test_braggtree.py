from __future__ import absolute_import, print_function
import unittest
from qtpy.QtWidgets import QApplication
from addie.rietveld.braggtree import BraggTree, BankRegexException


class BraggTreeTests(unittest.TestCase):
    def setUp(self):
        self.main_window = QApplication([])

    def test_get_bank_id(self):
        """Test we can extract a bank id from bank workspace name"""
        braggtree = BraggTree(None)
        target = 12345
        bank_wksp_name = "Bank {} - 90.0".format(target)
        bank_id = braggtree._get_bank_id(bank_wksp_name)
        self.assertEqual(int(bank_id), target)

    def test_get_bank_id_fails(self):
        """Test for failure of extracting bank id from bank workspace name"""
        braggtree = BraggTree(None)
        bad_wksp_name = "Bank jkl 1 -- 90.0"
        self.assertRaises(
            BankRegexException,
            braggtree._get_bank_id,
            bad_wksp_name)


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
