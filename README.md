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

A variant if you are using [anaconda](https://www.continuum.io/why-anaconda) is

1. `python setup.py pyuic`
1. `python setup.py install` (installs into anaconda's tree and sets up the environment)
3. `fastgr`

Creating RPMs
-------------

Python generated `srpm` are not as flexible as they should be. To
generate one that is:

1. Create a tarball using `python setup.py sdist`
2. Generate the spec file `python setup.py bdist_rpm --spec-only`
3. Edit the spec file to fix the release number and change the package name for `matplotlib` as it is different between rhel and fedora.
```
Release: %{release}%{?dist}

...

%if 0%{?rhel}
Requires: python numpy python-matplotlib PyQt4
%else
Requires: python numpy python2-matplotlib PyQt4
%endif
```
4. Copy the tarball into the correct place in `~/rpmbuild` and build it using the modified spec `rpmbuild -ba dist/fastgr.spec`

The `srpm` generated can be uploaded to [copr](http://copr.fedoraproject.org) to build for any platform.


[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](http://opensource.org/licenses/MIT)
