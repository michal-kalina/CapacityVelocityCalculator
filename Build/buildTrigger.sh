#!/bin/bash

# get buildTrigger.sh script location
SCRIPT_DIR=$( cd ${0%/*} && pwd -P )
cd $SCRIPT_DIR
echo "Start from root directory"
cd ..
pwd

echo "Try to remove venv folder"
rm -r venv

echo "Install virtual environment"
# instal virtual environment
python3 -m pip install --user virtualenv
# create virtual environment
python3 -m virtualenv venv
# enable venv environment
. venv/bin/activate

#ls -la

echo "Install python modules"
python3 -m pip install -r requirements.txt

echo "run project"
python3 Src/main.py