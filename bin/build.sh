#!/bin/bash -e
pip install -r requirements-test.txt
export $(cat .env.sample)
cd src && python -m pytest
cd ..
flake8 src
