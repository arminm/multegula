#!/bin/bash
###########################################################
#Multegula - run.sh                                       #
#Main Driver/Startup Script for Multegula                 #
#Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He#
###########################################################

#NOTES: run.sh will accept an arbitrary TCP port number for
#multiple local instances  (for testing)
#Use like this: "./run.sh 55555"

#Cleanup any running go
killall go 2> /dev/null
killall multegula 2> /dev/null
sleep 1

#Start multegula.go and wait for it to come up.
#Defaults to port 44444 if port isn't received.
go run multegula.go -port=${1:-44444} uiConfig &
sleep 4

#Start UI only if background "go run" job succeeded. Works by checking if we have a process ID.
#Defaults to port 44444 if port isn't received.
if kill -0 $!; then
    echo "Multegula core started successfully! Starting UI."
    python3 UI/multegulaUI.py ${1:-44444}
else
    echo "Multegula core failed to start!  Aborting UI."
fi
