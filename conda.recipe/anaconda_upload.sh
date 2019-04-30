#!/usr/bin/env bash

# Input
if [[ $# -ne 1 ]]
then
  echo "Usage: anaconda_upload.sh <python version>"
  exit 1
fi
export PYTHON_VERSION=$1

# Setup anaconda for upload.
#  NOTE: client set since there was a regression and this one shows errors.
conda config --set anaconda_upload no
conda install -q conda-build anaconda-client=1.5.5

# Function for building recipe and then uploading package:
# Usage example: conda_build_and_upload build_dir meta.yaml main
function conda_build_and_upload {
    if [[ $# -ne 2 ]]
    then
      echo "Usage: conda_build <os type> <package directory>"
      exit 1
    fi
    export OS=$1

	conda build conda.recipe --python=${PYTHON_VERSION}
    PKG_PATH=$(conda build conda.recipe --python=${PYTHON_VERSION} --output)
    PKG_FILE=$(basename ${PKG_PATH})

    echo "Uploading ${PKG_FILE} artifact..."
    anaconda -v -t ${CONDA_UPLOAD_TOKEN} upload ${PKG_PATH} --force
    echo "error code: $#"
    echo "Successfully deployed ${PKG_FILE} to Anaconda.org."
}

conda_build_and_upload ${TRAVIS_OS_NAME}-64 
