#!/bin/bash
###########################################################
#Multegula - run.sh                                       #
#Main Driver/Startup Script for Multegula                 #
#Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He#
###########################################################

#Cleanup any running go
killall go 2> /dev/null
killall multegula 2> /dev/null
sleep 1

bash -c 'go run multegula.go config bob' &
sleep 3

#Start UI only if background "go run" job succeeded. Works by checking if we have a process ID.
if kill -0 $!; then
    echo "Multegula core started successfully! Starting UI."
    python3 UI/multegulaUI.py
else
    echo "Multegula core failed to start!  Aborting UI."
fi
