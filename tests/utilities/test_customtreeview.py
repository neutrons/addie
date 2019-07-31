from __future__ import absolute_import, print_function
import unittest
from qtpy.QtWidgets import QApplication
from addie.utilities.customtreeview import CustomizedTreeView


class CustomTreeViewTests(unittest.TestCase):
    def setUp(self):
        self.main_window = QApplication([])
        
    def tearDown(self):
        self.main_window.quit()

    def test_construction(self):
        """Test construction of CustomizedTreeView"""
        treeview = CustomizedTreeView(None)

    def test_get_selected_items(self):
        """Test get_selected_items in tree of CustomizedTreeView"""
        treeview = CustomizedTreeView(None)
        items = treeview.get_selected_items()
        self.assertEqual(items, [])
        self.assertEqual(type(items), list)