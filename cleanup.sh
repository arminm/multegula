#!/bin/bash
###########################################################
#Multegula - cleanup.sh                                   #
#Cleanup script for running Multegula processes           #
#Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He#
###########################################################

echo "Cleaning up processes and sockets..."
#Cleanup any running go
pkill -9 go 2> /dev/null
pkill -9 multegula 2> /dev/null
pkill -9 bootstrap 2> /dev/null
pkill -9 BootstrapServer 2> /dev/null

####################################
##To be EXTRA clean - maybe remove these for release.
##We don't want users accidentally killing important processes.
####################################
pkill -9 -f python 2> /dev/null
pkill -9 -f python3 2> /dev/null
pkill -9 -f Python 2> /dev/null
pkill -9 -f Python3 2> /dev/null
#################################

echo "The light is green, the trap is clean."