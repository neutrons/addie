| CI     | Release | Other |
|--------|---------|-------|
| [![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fneutrons%2Faddie%2Fbadge&style=plastic)](https://actions-badge.atrox.dev/neutrons/addie/goto)  | [![Anaconda-Server Badge](https://anaconda.org/addie-diffraction/addie/badges/version.svg)](https://anaconda.org/addie-diffraction/addie) | [![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](http://opensource.org/licenses/MIT) |
|  | [![Anaconda-Server Badge](https://anaconda.org/addie-diffraction/addie/badges/platforms.svg)](https://anaconda.org/addie-diffraction/addie) | |

# ADDIE

**ADDIE** stands for **AD**vandced **DI**ffraction **E**nvironment, a data reduction application for total scattering powder diffraction data. 

The name came about from being developed for the Diffraction Group at SNS located at ORNL (and previously known as the Advanced Diffraction Group).

This "reduction" entails taking raw neutron counts from detectors in the diffraction experiment and turning them into the reciprocal-space structure factor patterns, F(Q) or S(Q), and applying a Fourier Transform to real-space to give the pair distribution fuction, PDF.

ADDIE is a front-end GUI for total scattering that hopes to support multiple diffractometers performing total scattering measurements. The back-end that uses the [Mantid Framework](https://docs.mantidproject.org/nightly/) is the [`mantid-total-scattering`](https://github.com/marshallmcdonnell/mantid_total_scattering) project.

## Installation

```
conda config --add channels conda-forge --add channels marshallmcdonnell --add channels mantid --add channels mantid/label/nightly
conda create -n addie_env python=${python_version}
source activate addie_env
```

## Launch 

To launch ADDIE, run the following from the command line:

```bash
addie
```

If you need to specify the path to Mantid build, use:
```
MANTIDPATH=/path/to/mantid/build/bin PATH=$MANTIDPATH:$PATH PYTHONPATH=$MANTIDPATH:$PATH addie
```


## Development


### Installation development environment using Conda
```
conda env create
source activate addie
python setup.py install
```

**Notes**

If you have an error (see below for example) related to the `libGL` library, you may not have it installed for the Mantid Framework to work. See instructions [here](https://github.com/mantidproject/conda-recipes/#gl-and-glu-libs) for installing the necessary libraries for different OS

Example error:
`ImportError: First import of "._api" failed with "libGL.so.1: cannot open shared object file...`


### Testing

The test suite can be run using [pytest](https://docs.pytest.org/en/latest/)
with the [pytest-qt](https://pytest-qt.readthedocs.io/en/latest/) plugin.
```bash
$ pytest tests
```


### Developing using a local Mantid install

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

## Creating RPMs

Python generated `srpm` are not as flexible as they should be. To
generate one that is run `buildrpm` and look for the files in the
`dist` directory.
```bash
$ ./buildrpm
```
 The `rpm`s are available on
[copr](https://copr.fedorainfracloud.org/coprs/peterfpeterson/addie/).


