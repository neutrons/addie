from __future__ import absolute_import, print_function
import unittest
import os

from addie.addiedriver import AddieDriver

DATA_DIR = os.path.dirname(__file__)
print('looking for data in "{}"'.format(DATA_DIR))


class readSofQ(unittest.TestCase):
    def setUp(self):
        self.datFiles = ['SofQ_NaNO3_230C.dat',
                         'SofQ_NaNO3_275C.dat']
        self.datFiles = [os.path.join(DATA_DIR, filename) for filename in self.datFiles]

        self.nxsFiles = []
        self.nxsFiles = [os.path.join(DATA_DIR, filename) for filename in self.nxsFiles]

    def runLoad(self, driver, filename):
        print('loading "{}"'.format(filename))
        wksp, qmin, qmax = driver.load_sq(filename)
        self.assertLess(qmin, qmax, 'qmin[{}] >= qmax[{}]'.format(qmin, qmax))
        # TODO actual checks on the workspace

    def test_dat(self):
        driver = AddieDriver()
        for filename in self.datFiles:
            self.runLoad(driver, filename)

    def test_nxs(self):
        driver = AddieDriver()
        for filename in self.nxsFiles:
            self.runLoad(driver, filename)


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
