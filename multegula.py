#!/usr/bin/python3
###########################################################
#Multegula - multegula.py                                 #
#Main Driver/Startup Script for Multegula                 #
#Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He#
###########################################################

#######IMPORTS#######
import subprocess #Needed for system calls
import time #Needed to sleep
from multiprocessing import Process #Needed to spawn another thread
from UI.multegulaUI import * #Import our UI functions
#####################

#Start PyBridge, and give it time to come up before continuing
PyBridge = subprocess.Popen(['go', 'run', 'multegula.go', 'config', 'bob'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
time.sleep(1)

#Start UI
runUI(sys.argv)

#Start both functions simultaneously
p1 = Process(target=runUI(sys.argv))
p2 = Process(target=receiveThread)
p1.start()
p2.start()
p1.join()
p2.join()
