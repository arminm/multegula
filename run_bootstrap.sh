#!/bin/bash
###########################################################
#Multegula - run_bootstrap.sh                             #
#Startup Script for Multegula Bootstrap Server            #
#Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He#
###########################################################

#Cleanup any running go
killall go 2> /dev/null
killall multegula 2> /dev/null
killall BootstrapServer 2> /dev/null
sleep 1

#Start multegula.go and wait for it to come up.
#Defaults to port 55555 if port isn't received.
go run bootstrapServer/bootstrapServer.go -port=${1:-55555}
