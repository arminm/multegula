#!/bin/bash

NODES=(armin lunwen daniel garrett)

##############################
# Modify these parameters:
PWD=~/go/src/github.com/arminm/multegula
CONFIG_FILE_NAME=localConfig

##############################
#Cleanup any running go
killall go 2> /dev/null
killall multegula 2> /dev/null
sleep 1

##############################
# generate launcher files
for i in "${NODES[@]}"; do
    echo \#\!/bin/bash > $i.sh
    echo cd $PWD >> $i.sh
    echo go run multegula.go -test $CONFIG_FILE_NAME $i >> $i.sh
    chmod +rwx $i.sh
done

##############################
# Run launcher files

for i in "${NODES[@]}"; do
    echo launching $i
    x-terminal-emulator -e bash $i.sh
done

sleep 1
##############################
# Clean launcher files (may not be necessary)

for i in "${NODES[@]}"; do
    echo removing $i
    rm $i.sh
done
