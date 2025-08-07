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

### Pre-requisite: Install Pixi

Please follow the instructions provided at https://pixi.sh/latest/installation/

### Install the Pixi Environment

In the root of the repo:

```
pixi install
```

If you would just like to import the package into your own conda environement
then simply run the following instead.

Install ADDIE in the conda environment:
```
mamba install -c neutrons addie
```

## Uninstall

For Pixi simply delete the `.pixi` folder it generates in the repo root.

For Conda:
```
mamba remove addie
```

## Launch

To launch ADDIE, run the following from the command line:

```bash
pixi run addie
```

If you need to specify the path to Mantid build.
In the pyproject.toml file 
update `MANTID_BUILD_DIR` to point to your build directory
and  `MANTID_SRC_DIR` to point to your source directory.
```
pixi run addie-local-mantid
```


## Development


### Installation development environment using Pixi

```bash
pixi install
```

This will setup all the dependencies necessary to develop ADDIE.

Then suppose one is located in the main directory of the ADDIE repo, executing
the following command will start up ADDIE,

```bash
pixi run python addie/main.py
```

or just

```bash
pixi run addie
```

> N.B. If the drive mounting point on the operating system is changed, we may to
rerun the setup above. Otherwise, even though the soft link may still point to
the right locations, we may encounter the file permission issues when trying to
launch the `ADDIE` GUI.

### Uninstall

Simply delete the `.pixi` folder.

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

The test suite can be run using [pytest](https://docs.pytest.org/en/latest/) through pixi.
```bash
$ pixi run test
```
If it is complaining about not being able to find the `pytest` module, first we
need to make sure we have installed the pixi environment.

### Some cheat sheet commands for running pixi

```bash
pixi shell  # activate the pixi shell, something analogous to `conda activate`
addie  # the command is only available when pixi shell is active
exit  # exit the pixi shell
pixi run addie  # run application task without activating pixi shell
pixi run link  # specifically defined link task
pixi shell -e local-mantid  # activate the pixi shell with the `local-mantid` environment
```
