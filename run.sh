#!/bin/bash
###########################################################
#Multegula - run.sh                                       #
#Main Driver/Startup Script for Multegula                 #
#Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He#
###########################################################

#NOTES: run.sh will accept an arbitrary TCP port number for
#multiple local instances  (for testing)
#Use like this: "./run.sh <UI Port> <Game Port>".
#Defaults are:              44444     1111
#Arguments are optional.

#Cleanup any running go
pkill -9 go 2> /dev/null
pkill -9 multegula 2> /dev/null
pkill -9 bootstrap 2> /dev/null
pkill -9 BootstrapServer 2> /dev/null
pkill -9 -f multegulaUI.py 2> /dev/null

####################################
##To be EXTRA clean - maybe remove these for release.
##We don't want users accidentally killing important processes.
####################################
pkill -9 -f python 2> /dev/null
pkill -9 -f python3 2> /dev/null
pkill -9 -f Python 2> /dev/null
pkill -9 -f Python3 2> /dev/null
#################################

sleep 1

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
