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
##To be EXTRA clean - maybe remove these for release
####################################
pkill -9 python 2> /dev/null
pkill -9 python3 2> /dev/null
#################################

echo "The light is green, the trap is clean."