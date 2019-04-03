#!/usr/bin/env bash
# For the first time, use this
#git submodule update --init --recursive

# To pull the last commit on all submodules
git submodule foreach git pull origin master
