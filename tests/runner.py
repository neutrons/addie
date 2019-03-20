from __future__ import absolute_import, print_function
import sys
import unittest

# import test modules
from tests import \
    test_fileio

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_fileio))

# initialize a runner and run it
runner = unittest.TextTestRunner(verbosity=3, buffer=True)
result = runner.run(suite).wasSuccessful()
sys.exit(not result)  # weird "opposite" logic
