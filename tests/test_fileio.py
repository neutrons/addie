from __future__ import absolute_import, print_function
import numpy as np
import os
import unittest
from mantid.simpleapi import mtd
from addie.addiedriver import AddieDriver

from tests import DATA_DIR


def expectedWkspName(filename):
    return os.path.basename(filename).split('.')[0]


class readGofr(unittest.TestCase):
    def setUp(self):
        self.files = ['NOM_127827.gr']
        self.files = [os.path.join(DATA_DIR, filename) for filename in self.files]

    def test(self):
        driver = AddieDriver()
        for filename in self.files:
            worked, wkspname = driver.load_gr(filename)
            self.assertEquals(wkspname, expectedWkspName(filename))
            # TODO actual checks on the workspace


class readSofQ(unittest.TestCase):
    def setUp(self):
        self.datFiles = ['SofQ_NaNO3_230C.dat',
                         'SofQ_NaNO3_275C.dat']
        self.datFiles = [os.path.join(DATA_DIR, filename) for filename in self.datFiles]

        self.nxsFiles = ['NOM_127827_SQ.nxs']
        self.nxsFiles = [os.path.join(DATA_DIR, filename) for filename in self.nxsFiles]

    def runLoad(self, driver, filename):
        print('loading "{}"'.format(filename))
        wksp, qmin, qmax = driver.load_sq(filename)
        self.assertLess(qmin, qmax, 'qmin[{}] >= qmax[{}]'.format(qmin, qmax))
        self.assertEquals(str(wksp), expectedWkspName(filename))
        # TODO actual checks on the workspace
        self.assertAlmostEqual(np.average(mtd[wksp].readY(0)[-100:]), 1., places=1)

    def test_dat(self):
        driver = AddieDriver()
        for filename in self.datFiles:
            self.runLoad(driver, filename)

    def test_nxs(self):
        driver = AddieDriver()
        for filename in self.nxsFiles:
            self.runLoad(driver, filename)


class readGSAS(unittest.TestCase):
    def setUp(self):
        self.files = ['NOM_127827.gsa']
        self.files = [os.path.join(DATA_DIR, filename) for filename in self.files]

    def test(self):
        driver = AddieDriver()
        for filename in self.files:
            wkspname = driver.load_bragg_file(filename)
            self.assertEquals(wkspname, expectedWkspName(filename))
            # TODO actual checks on the workspace

if __name__ == '__main__':
    unittest.main()  # pragma: no cover
