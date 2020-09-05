#!/bin/bash

for var in `ls`;
do
    echo $var | grep -q "\." && a=1 || a=0
    if [ $a = 0 ] ; then
        echo $var
        rm -rf $var/__pycache__
    fi
done
