#!/bin/bash

NAME=$1
BNAME=$(basename $NAME .zip )
mkdir -p $BNAME 
cd $BNAME
rm -rf *
unzip ../$NAME 
