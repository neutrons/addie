from __future__ import absolute_import, print_function
import unittest
import os

from addie.addiedriver import AddieDriver
from tests import DATA_DIR

TOF = 'TOF'
D_SPACING = 'dSpacing'
Q_SPACE = 'MomentumTransfer'


class BraggData(unittest.TestCase):
    def setUp(self):
        self.filename = os.path.join(DATA_DIR, 'NOM_127827.gsa')

    def test_get_data(self):
        driver = AddieDriver()
        # load the data
        wkspname = driver.load_bragg_file(self.filename)

        # create a bunch of individual spectra
        # FIXME should just use the original workspace itself
        groupWkspName, banks_list, bank_angles = driver.split_to_single_bank(wkspname)
        print(wkspname, groupWkspName)

        for units in (TOF, D_SPACING, Q_SPACE):
            for wkspIndex in range(6):
                x, y, dy = driver.get_bragg_data(groupWkspName, wkspIndex + 1, units)
                self.assertEqual(len(x), len(y))
                self.assertEqual(len(y), len(dy))
                self.assertLess(x[0], x[-1], 'xmin[{}] >= xmax[{}]'.format(x[0], x[-1]))
                if units == TOF:  # these values are copied from the GSAS file
                    if wkspIndex == 0:
                        self.assertEqual(x[0], 743.140027596)
                        self.assertEqual(x[-1], 8971.042698148)
                    elif wkspIndex == 1:
                        self.assertEqual(x[0], 887.289527377)
                        self.assertEqual(x[-1], 17966.432721196)
                    elif wkspIndex == 2:
                        self.assertEqual(x[0], 1009.427358717)
                        self.assertEqual(x[-1], 19058.487769870)
                    elif wkspIndex == 3:
                        self.assertEqual(x[0], 1175.684429098)
                        self.assertEqual(x[-1], 17176.602366475)
                    elif wkspIndex == 4:
                        self.assertEqual(x[0], 1288.635270161)
                        self.assertEqual(x[-1], 15260.397565064)
                    elif wkspIndex == 5:
                        self.assertEqual(x[0], 858.293757585)
                        self.assertEqual(x[-1], 10270.673982962)


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
