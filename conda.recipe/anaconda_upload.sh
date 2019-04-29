#!/usr/bin/env bash

# Inputs
OS=${TRAVIS_OS_NAME}-64

# Setup anaconda for upload.
#  NOTE: client set since there was a regression and this one shows errors.
conda config --set anaconda_upload no
conda install -q conda-build anaconda-client=1.5.5

# Function for building recipe and then uploading package:
# Usage example: conda_build_and_upload build_dir meta.yaml main
function conda_build_and_upload {
    if [[ $# -ne 1 ]]
    then
      echo "Usage: conda_build <package directory>"
      exit 1
    fi

    export PKG_NAME=$1

	export CONDA_BLD_PATH=$HOME/conda-bld
    rm -rf ${CONDA_BLD_PATH}
	mkdir ${CONDA_BLD_PATH}

	conda build .
	
	export BUILD=$(ls ${CONDA_BLD_PATH}/${OS}/${PKG_NAME}* | sed -n "s/.*${PKG_NAME}-\(.*\)-\(.*\)\.tar.bz2/\1-\2/p")
	echo "Uploading ${PKG_NAME}-${BUILD}.tar.bz2 artifact..."
	anaconda -v -t ${CONDA_UPLOAD_TOKEN} upload ${CONDA_BLD_PATH}/${OS}/${PKG_NAME}-${BUILD}.tar.bz2 --force

	echo "Successfully deployed ${PKG_NAME}-${BUILD} to Anaconda.org."
}

conda_build_and_upload addie
