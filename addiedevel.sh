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

# get the python version to add to the PYTHONPATH
# the double-bracket thing isn't pure bash but will work on most os
if [ "$CMD" == "*mantidpython*" ]; then
    RAW_PYTHON=$(grep python $CMD | grep set | tail -n 1 | awk '{print $3}')
else
    RAW_PYTHON=$CMD
fi
PYTHON_VERSION=$($RAW_PYTHON -c 'import sys; version=sys.version_info[:3]; print("{0}.{1}".format(*version))')
echo using $RAW_PYTHON version $PYTHON_VERSION

# build the package
$CMD setup.py build

# launch addie
QT_API=$LOCAL_QT_API PYTHONPATH=build/lib:$PYTHONPATH $CMD build/scripts-${PYTHON_VERSION}/addie
