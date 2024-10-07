from __future__ import absolute_import, print_function
import numpy as np
import os
import unittest
from mantid.simpleapi import mtd
from addie.addiedriver import AddieDriver
from addie.rietveld.event_handler import load_bragg_by_filename

from tests import DATA_DIR

TOF = 'TOF'
D_SPACING = 'dSpacing'
Q_SPACE = 'MomentumTransfer'


def expectedWkspName(filename):
    return os.path.basename(filename).split('.')[0]


class AddieDriverLoadGofRTests(unittest.TestCase):
    def setUp(self):
        self.files = ['NOM_127827.gr']
        self.files = [os.path.join(DATA_DIR, filename) for filename in self.files]

    def test_load_gr_gr_files(self):
        """Test that we can load G(r) *.gr files"""
        driver = AddieDriver()
        for filename in self.files:
            worked, wkspname = driver.load_gr(filename)
            self.assertEqual(wkspname, expectedWkspName(filename))
            # TODO actual checks on the workspace


class AddieDriverLoadSofQTests(unittest.TestCase):
    def setUp(self):
        self.datFiles = ['SofQ_NaNO3_230C.dat',
                         'SofQ_NaNO3_275C.dat']
        self.datFiles = [os.path.join(DATA_DIR, filename) for filename in self.datFiles]

        self.nxsFiles = ['NOM_127827_SQ.nxs']
        self.nxsFiles = [os.path.join(DATA_DIR, filename) for filename in self.nxsFiles]

    def runLoad(self, driver, filename):
        """Utility for testing load of S(Q) files"""
        print('loading "{}"'.format(filename))
        wksp, qmin, qmax = driver.load_sq(filename)
        self.assertLess(qmin, qmax, 'qmin[{}] >= qmax[{}]'.format(qmin, qmax))
        self.assertEqual(str(wksp), expectedWkspName(filename))
        # TODO actual checks on the workspace
        self.assertAlmostEqual(np.average(mtd[wksp].readY(0)[-100:]), 0., places=1)

    def test_load_sq_dat_files(self):
        """Test that we can load S(Q) *.dat files"""
        driver = AddieDriver()
        for filename in self.datFiles:
            self.runLoad(driver, filename)

    def test_load_sq_nxs_files(self):
        """Test that we can load S(Q) *.nxs (NeXus) files"""
        driver = AddieDriver()
        for filename in self.nxsFiles:
            self.runLoad(driver, filename)


class AddieDriverBraggDataTests(unittest.TestCase):
    def setUp(self):
        self.filename = os.path.join(DATA_DIR, 'NOM_127827.gsa')
        self.files = [self.filename]
        self.files = [os.path.join(DATA_DIR, filename) for filename in self.files]

    def test_get_data(self):
        driver = AddieDriver()
        # load the data
        wkspname, bank_angles = load_bragg_by_filename(self.filename)

        for units in (TOF, D_SPACING, Q_SPACE):
            for wkspIndex in range(6):
                # TODO this method should be removed from AddieDriver
                x, y, dy = driver.get_bragg_data(wkspname, wkspIndex, units)
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
