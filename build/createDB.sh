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
echo "Create DB"
python3 src/web/manage.py migrate