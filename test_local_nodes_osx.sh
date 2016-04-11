#!/bin/bash

NODES=(armin lunwen daniel garrett)

##############################
# Modify these parameters:
PWD=~/go/src/github.com/arminm/multegula
CONFIG_FILE_NAME=localConfig

##############################
# generate launcher files
for i in "${NODES[@]}"; do
    echo \#\!/bin/bash > $i.sh
    echo cd $PWD >> $i.sh
    echo go run multegula.go -test $CONFIG_FILE_NAME $i >> $i.sh
    chmod +rwx $i.sh
done

##############################
# Clean launcher files

for i in "${NODES[@]}"; do
    echo launching $i
    open -a Terminal $i.sh
done

sleep 1
##############################
# Clean launcher files (may not be necessary)

for i in "${NODES[@]}"; do
    echo removing $i
    rm $i.sh
done
