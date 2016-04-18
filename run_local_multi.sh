#!/bin/bash
###########################################################
#Multegula - run_local_multi.sh                           #
#Startup Script for Local Multegula Hosts                 #
#Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He#
###########################################################

#Cleanup any running go
killall go 2> /dev/null
killall multegula 2> /dev/null
killall BootstrapServer 2> /dev/null
sleep 1
#=======================================
# CLIENT 1
#=======================================
#Start multegula.go and wait for it to come up.
go run multegula.go -uiport=${1:-11111} -gameport=${2:-1111} &
sleep 4

#Start UI only if background "go run" job succeeded. Works by checking if we have a process ID.
if kill -0 $!; then
    echo "Multegula core started successfully! Starting UI."
    python3 UI/multegulaUI.py ${1:-11111} &
else
    echo "Multegula core failed to start!  Aborting UI."
fi
#=======================================
# CLIENT 2
#=======================================
#Start multegula.go and wait for it to come up.
go run multegula.go -uiport=${1:-22222} -gameport=${2:-2222} &
sleep 4

#Start UI only if background "go run" job succeeded. Works by checking if we have a process ID.
if kill -0 $!; then
    echo "Multegula core started successfully! Starting UI."
    python3 UI/multegulaUI.py ${1:-22222} &
else
    echo "Multegula core failed to start!  Aborting UI."
fi
#=======================================
# CLIENT 3
#=======================================
#Start multegula.go and wait for it to come up.
go run multegula.go -uiport=${1:-33333} -gameport=${2:-3333} &
sleep 4

#Start UI only if background "go run" job succeeded. Works by checking if we have a process ID.
if kill -0 $!; then
    echo "Multegula core started successfully! Starting UI."
    python3 UI/multegulaUI.py ${1:-33333} &
else
    echo "Multegula core failed to start!  Aborting UI."
fi

#=======================================
# CLIENT 4
#=======================================
#Start multegula.go and wait for it to come up.
go run multegula.go -uiport=${1:-44444} -gameport=${2:-4444} &
sleep 4

#Start UI only if background "go run" job succeeded. Works by checking if we have a process ID.
if kill -0 $!; then
    echo "Multegula core started successfully! Starting UI."
    python3 UI/multegulaUI.py ${1:-44444}
else
    echo "Multegula core failed to start!  Aborting UI."
fi