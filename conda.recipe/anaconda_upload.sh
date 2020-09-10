#!/usr/bin/env bash
  

conda install conda-build conda-verify anaconda-client 
conda build . 

export PKG_PATH=$(conda build . --output)
PKG_FILE=$(basename ${PKG_PATH})
echo ${PKG_FILE}
echo ${PKG_PATH}

echo "Uploading ${PKG_PATH} artifact..."
anaconda -v -t ${CONDA_UPLOAD_TOKEN} upload ${PKG_PATH} --force

echo "Successfully deployed ${PKG_FILE} to Anaconda.org."
