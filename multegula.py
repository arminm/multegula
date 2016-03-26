#!/usr/bin/python3
###########################################################
#Multegula - multegula.py                                 #
#Main Driver/Startup Script for Multegula                 #
#Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He#
###########################################################

import sys

#Tells Python to search multegulaUI folder for functions as well.
sys.path.append('multegulaUI/')

from multegulaUI.multegulaUI import * #Import our UI functions
import subprocess #Needed for system calls
from multiprocessing import Process #Needed for function concurrency

#Start MessagePasser
messagepasser = subprocess.Popen(['go', 'run', 'MessagePasser.go'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

#Start UI
p1 = Process(target=runUI)
p1.start()
p1.join()
