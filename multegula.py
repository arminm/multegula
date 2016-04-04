#!/usr/bin/python3
###########################################################
#Multegula - multegula.py                                 #
#Main Driver/Startup Script for Multegula                 #
#Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He#
###########################################################

#######IMPORTS#######
import sys #Needs to be here before the path append.
import subprocess #Needed for system calls
from multiprocessing import Process #Needed for function concurrency
import time #Needed to sleep
#####################

#Tells Python to search UI and Bridges folder for functions as well.
sys.path.append('UI/')
sys.path.append('Bridges/')

#####OUR IMPORTS#####
from UI.multegulaUI import * #Import our UI functions
from Bridges.GoBridge import * #Import our Go Bridge
#####################

#Start PyBridge, and give it time to come up before continuing
PyBridge = subprocess.Popen(['go', 'run', 'Bridges/PyBridge.go'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
time.sleep(1)

#Start UI
p1 = Process(target=runGoBridge)
p2 = Process(target=runUI)
p1.start()
p2.start()
p1.join()
p2.join()
