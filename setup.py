# this file is necessary so conda can read the contents of setup.cfg using
# its load_setup_py_data function
from setuptools import setup
from versioningit import get_cmdclasses

setup(cmdclass=get_cmdclasses())
