from __future__ import absolute_import, print_function
import os

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(TEST_DIR, "test_files")
IMAGE_DIR = os.path.join(TEST_DIR, "mpl_files")
print('looking for data in "{}"'.format(DATA_DIR))
