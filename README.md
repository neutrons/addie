FastGR
======

Lots of wonderful text about this being a GUI to do a Fourier transform.

Building
--------

Before doing the normal `python setup.py ...` things you must convert the
`designer/*.ui` files to `fastgr*.py`. This is done with
`python setup.py pyuic`. After that, all the normal
[setuptools](https://pythonhosted.org/setuptools/setuptools.html) magic applies.

To run from source (step 1 only needs to be done if the `.ui` file changes):

1. `python setup.py pyuic` (does nothing unless `.ui` file changes)
1. `python setup.py build`
3. `PYTHONPATH=build/lib:$PYTHONPATH build/scripts-2.7/fastgr` (puts
   build directory into your `PYTHONPATH` for that execution only)

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](http://opensource.org/licenses/MIT)
