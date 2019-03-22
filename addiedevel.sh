#!/bin/sh

# select qt version
if [ -n "${QT_API}" ]; then
    LOCAL_QT_API=${QT_API}
else
    LOCAL_QT_API="pyqt5"
fi

# select the python to start with
if [ -n "$1" ]; then
    CMD="$@"
elif [ "$(command -v mantidpythonnightly --classic)" ]; then
    CMD="$(command -v mantidpythonnightly) --classic"
else
    CMD="$(command -v mantidpython) --classic"
fi

PYTHON_VERSION=`$CMD -c 'import sys; version=sys.version_info[:3]; print("{0}.{1}".format(*version))'`
$CMD setup.py build

# launch addie
QT_API=$LOCAL_QT_API PYTHONPATH=build/lib:$PYTHONPATH $CMD build/scripts-${PYTHON_VERSION}/addie --mode 'idl'
