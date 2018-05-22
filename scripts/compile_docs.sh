#!/bin/bash

BASE_DIR=`dirname $(readlink -f $0)`/..
cd $BASE_DIR/doc
make html
