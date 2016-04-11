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
go run multegula.go config bob ${1:-44444} &
sleep 3

#Start UI only if background "go run" job succeeded. Works by checking if we have a process ID.
if kill -0 $!; then
    echo "Multegula core started successfully! Starting UI."
    python3 UI/multegulaUI.py ${1:-44444}
else
    echo "Multegula core failed to start!  Aborting UI."
fi
