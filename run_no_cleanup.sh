#!/bin/bash
###########################################################
#Multegula - run.sh                                       #
#Main Driver/Startup Script for Multegula                 #
#Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He#
###########################################################

#Start multegula.go and wait for it to come up.
#Defaults to port 44444 if port isn't received.
go run multegula.go -uiport=${1:-44444} -gameport=${2:-11111} &
sleep 4

#Start UI only if background "go run" job succeeded. Works by checking if we have a process ID.
#Defaults to port 44444 if port isn't received.
if kill -0 $!; then
    echo "Multegula core started successfully! Starting UI."
    python3 UI/multegulaUI.py ${1:-44444}
else
    echo "Multegula core failed to start!  Aborting UI."
fi
