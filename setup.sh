#! /bin/bash

export PYTHONWARNINGS="ignore"
rm -rf venv
python3 -m venv venv/
source venv/bin/activate
pip3 install boto3

python3 setup_lab.py
