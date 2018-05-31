#!/bin/bash

BASE_DIR=`dirname $(readlink -f $0)`/..
cp -R $BASE_DIR/hooks/* $BASE_DIR/.git/hooks/