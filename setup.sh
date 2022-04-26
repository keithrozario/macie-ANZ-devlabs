#! /bin/bash

export PYTHONWARNINGS="ignore"
pip3 install boto3 --quiet

python3 setup_lab.py
