#!/bin/sh
python setup.py build

PYTHON_VERSION=`python -c 'import sys; version=sys.version_info[:3]; print("{0}.{1}".format(*version))'`

if [ $1 ]; then
    CMD=$1
else
    CMD=''
fi
PYTHONPATH=build/lib:$PYTHONPATH $CMD build/scripts-${PYTHON_VERSION}/addie
