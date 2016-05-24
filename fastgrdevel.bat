@echo off
setlocal enableextensions

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: Runs setuptools to put things into the build area
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
python setup.py pyuic
python setup.py build

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: Sets the required environment variables for the Python to run correctly.
:: All variables that are passed to this script are passed directly to
:: python.exe
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
set PYTHONPATH=build\lib\python-2.7\;%PYTHONPATH%
C:\MantidInstall\bin\mantidpython build\scripts\fastgr
