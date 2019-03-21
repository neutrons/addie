[![Build Status](https://travis-ci.org/neutrons/addie.svg?branch=master)](https://travis-ci.org/neutrons/addie)

Addie
======

Lots of wonderful text about this being a GUI to do a Fourier transform.


Building
--------

Before doing the normal `python setup.py ...` things you must convert the
`designer/*.ui` files to `addie*.py`. This is done with
`python setup.py pyuic`. After that, all the normal
[setuptools](https://pythonhosted.org/setuptools/setuptools.html) magic applies.

To run from source (step 1 only needs to be done if the `.ui` file changes):
```bash
$ addiedevel.sh
```
If you are want to specify a different `mantidpython`, then add it as
a command line argument
```bash
$ addiedevel.sh /opt/mantid37/bin/mantidpython
```

Similarly, there is a script for windows (experimental)
```
addiedevel.bat
```

The test suite can be run using unittests `discover` mode on the `tests` module
```bash
$ python -m unittest discover tests
```
or through the `setup.py` script
```bash
$ python setup.py test
```
Individual test files can be run directly as
```bash
$ python tests/test_fileio.py
```


Developing using virtual environments
-------------------------------------

If you normally develop using `virtualenv` or friends, you can develop
addie that way as well. After creating the virtual environment, run

```bash
<MANTIDBUILDDIR>/bin/AddPythonPath.py
```

which will add a file, `mantid.pth` to your environment with the
location of mantid. Then the normal

```bash
python setup.py develop
```

will put the rest of addie into your environment so you only need to
edit files and type `addie`.

As an extra reference, use [direnv](https://github.com/direnv/direnv)
to manange your virtual environments. For a python2 virtual
environment the `.envrc` file should contain
```
layout python2 -- --system-site-packages
```
so the system wide packages installed for mantid are found.

Creating RPMs
-------------

Python generated `srpm` are not as flexible as they should be. To
generate one that is run `buildrpm` and look for the files in the
`dist` directory.
```bash
$ ./buildrpm
```
 The `rpm`s are available on
[copr](https://copr.fedorainfracloud.org/coprs/peterfpeterson/addie/).


[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](http://opensource.org/licenses/MIT)
