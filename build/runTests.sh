#!/bin/bash

# get buildTrigger.sh script location
SCRIPT_DIR=$( cd ${0%/*} && pwd -P )
cd $SCRIPT_DIR
echo "Start from root directory"
cd ..
pwd

echo "Activate venv"
# enable venv environment
. venv/bin/activate
echo "============================"
python3 -m coverage run -m pytest
python3 -m coverage report --show-missing --skip-covered --skip-empty