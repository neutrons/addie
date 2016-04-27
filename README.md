FastGR
======

Lots of wonderful text about this being a GUI to do a Fourier transform.

Building
--------

Before doing the normal `python setup.py ...` things you must convert the
`designer/*.ui` files to `fastgr*.py`. This is done with
`python setup.py pyuic`. After that, all the normal
[setuptools](https://pythonhosted.org/setuptools/setuptools.html) magic applies.

Creating rpms
-------------

1. Create the `.py` files via `python setup.py pyuic`
2. Create a source distribution `python setup.py sdist`
3. Copy the tarball into `~/rpmbuild/SOURCES
4. Run `rpmbuild -ba fastgr.spec`


[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](http://opensource.org/licenses/MIT)
