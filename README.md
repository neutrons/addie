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
```bash
$ fastgrdevel.sh
```
If you are want to specify a different `mantidpython`, then add it as
a command line argument
```bash
$ fastgrdevel.sh /opt/mantid37/bin/mantidpython
```

Similarly, there is a script for windows (experimental)
```
fastgrdevel.bat
```

Creating RPMs
-------------

Python generated `srpm` are not as flexible as they should be. To
generate one that is run `buildrpm` and look for the files in the
`dist` directory.
```bash
$ ./buildrpm
```
 The `rpm`s are available on
[copr](https://copr.fedorainfracloud.org/coprs/peterfpeterson/fastgr/).


[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](http://opensource.org/licenses/MIT)
