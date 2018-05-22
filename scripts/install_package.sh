#!/bin/bash

BASE_DIR=`dirname $(readlink -f $0)`/..
cd $BASE_DIR/doc
mkdir $BASE_DIR/build
python $BASE_DIR/setup.py sdist
pip install -U --user -b $BASE_DIR/build $BASE_DIR/dist/*
rm -R $BASE_DIR/dist
rm -R $BASE_DIR/*.egg-info
rm -R $BASE_DIR/build