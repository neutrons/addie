#!/bin/sh
if [[ ! -d mantid_total_scattering ]]; then
    git submodule init
fi
git submodule update
