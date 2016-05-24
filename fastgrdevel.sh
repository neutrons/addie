#!/bin/sh
python setup.py pyuic
python setup.py build
if [ $1 ]; then
    CMD=$1
else
    CMD=''
fi
PYTHONPATH=build/lib:$PYTHONPATH $CMD build/scripts-2.7/fastgr
