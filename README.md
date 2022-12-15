| CI     | Release | Other |
|--------|---------|-------|
| [![GitHub Actions](https://github.com/neutrons/addie/actions/workflows/actions.yml/badge.svg?branch=master)](https://github.com/neutrons/addie/actions/workflows/actions.yml) | [![Anaconda-Server Badge](https://anaconda.org/neutrons/addie/badges/version.svg)](https://anaconda.org/neutrons/addie) | [![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](http://opensource.org/licenses/MIT) |
|  | [![Anaconda-Server Badge](https://anaconda.org/neutrons/addie/badges/platforms.svg)](https://anaconda.org/neutrons/addie) |





# ADDIE

**ADDIE** stands for **AD**vandced **DI**ffraction **E**nvironment,
a data reduction application for total scattering powder diffraction data.

The name came about from being developed for the Diffraction Group
at SNS located at ORNL (and previously known as the Advanced Diffraction Group).

This "reduction" entails taking raw neutron counts from detectors
in the diffraction experiment and turning them into the
reciprocal-space structure factor patterns, F(Q) or S(Q),
and applying a Fourier Transform to real-space to give
the pair distribution fuction, PDF.

ADDIE is a front-end GUI for total scattering that hopes to support
multiple diffractometers performing total scattering measurements.
The back-end that uses the
[Mantid Framework](https://docs.mantidproject.org/nightly/)
is the [`mantid-total-scattering`](https://github.com/neutrons/mantid_total_scattering)
project.

## Install

Setup conda environment to install ADDIE into:
```
conda create -n addie-env
conda activate addie-env
```

Install ADDIE in the conda environment:
```
conda install -c neutrons addie
```

## Uninstall

```
conda deactivate
conda remove -n addie_env --all
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

```bash
conda env create --file environment.yml
conda activate addie
pip install -e .
```

This will use the configuration in the `environment.yml` file for setting up the
`addie` conda environment. If one needs to change the conda environment name,
simply edit the `addie` to something else in the `environment.yml` file.

Then suppose one is located in the main directory of the ADDIE repo, executing
the following command will start up ADDIE,

```bash
python addie/main.py
```

or just

```bash
addie
```

### Uninstall

```bash
conda deactivate
conda remove -n addie --all
```

**Notes**

If you have an error (see below for example) related to the `libGL` library,
you may not have it installed for the Mantid Framework to work.
See instructions
[here](https://github.com/mantidproject/conda-recipes/#gl-and-glu-libs)
for installing the necessary libraries for different OS

Example error:

```
ImportError: First import of "._api" failed with "libGL.so.1: cannot open shared object file...
```

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

or with `pipenv` (which will use Pipfile),
first setup the directory and then add the `.envrc` file:
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
