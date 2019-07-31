from __future__ import absolute_import, print_function
import unittest
from qtpy.QtWidgets import QApplication
from addie.rietveld import event_handler


class RietveldEventHandlerTests(unittest.TestCase):
    def setUp(self):
        self.main_window = QApplication([])

    '''
    def tearDown(self):
        self.main_window.quit()
    '''

    def test_evt_change_gss_mode(self):
        """Test we can extract a bank id from bank workspace name"""
        f = event_handler.evt_change_gss_mode
        self.assertRaises(NotImplementedError, f, None)


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
