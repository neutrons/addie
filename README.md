[![Build Status](https://travis-ci.org/neutrons/addie.svg?branch=master)](https://travis-ci.org/neutrons/addie)

ADDIE
======

**ADDIE** stands for **AD**vandced **DI**ffraction **E**nvironment, a data reduction application for total scattering powder diffraction data. 

The name came about from being developed for the Diffraction Group at SNS located at ORNL (and previously known as the Advanced Diffraction Group).

This "reduction" entails taking raw neutron counts from detectors in the diffraction experiment and turning them into the reciprocal-space structure factor patterns, F(Q) or S(Q), and applying a Fourier Transform to real-space to give the pair distribution fuction, PDF.

ADDIE is a front-end GUI for total scattering that hopes to support multiple diffractometers performing total scattering measurements. The back-end that uses the [Mantid Framework](https://docs.mantidproject.org/nightly/) is the [`mantid-total-scattering`](https://github.com/marshallmcdonnell/mantid_total_scattering) project.

Installation
------------

### Anaconda
(coming soon)


Development
------------

### Building

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

The test suite can be run using [unittests](https://docs.python.org/3/library/unittest.html) `discover` mode on the `tests` module
```bash
$ python -m unittest discover
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
location of mantid. Then you need to setup for development: 

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

or with `pipenv` (which will use Pipfile), first setup the directory and then add the `.envrc` file:
```
cd addie
pipenv --two
echo layout_pipenv > .envrc
direnv allow
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
[copr](https://copr.fedorainfracloud.org/coprs/peterfpeterson/addie/).


[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](http://opensource.org/licenses/MIT)
