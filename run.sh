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

#Start PyBridge, and give it time to come up before continuing
go run multegula.go config bob &
sleep 2
python3 UI/multegulaUI.py -mid
