#!/usr/bin/env bash
  
# Input
if [[ $# -ne 1 ]]
then
  echo "Usage: anaconda_upload.sh <full package path>"
  exit 1
fi

PKG_PATH=$1
PKG_FILE=$(basename ${PKG_PATH})

echo "Uploading ${PKG_PATH} artifact..."
anaconda -v -t ${CONDA_UPLOAD_TOKEN} upload ${PKG_PATH} --force

echo "Successfully deployed ${PKG_FILE} to Anaconda.org."
