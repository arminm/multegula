###########################################################
#Multegula - GoBridge.py                                  #
#Functions to create local socket and messages            #
#Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He#
###########################################################

import socket
import time #Needed for labeling date/time
import datetime #Needed for labeling date/time

#Set arbitrary buffer size for received messages
BUFFER_SIZE = 200
DELIMITER = "##"

## RUN the GoBridge
## # this function starts the GoBridge running
def runGoBridge():
	#Get Time
	timestamp = int(time.time())
	prettytime = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
	
	#Set up the connection
	MessagePasser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		#Try to open connection to local Go MessagePasser
		MessagePasser.connect("127.0.0.1", "44444")
	except:
		print("[" + prettytime + "] Can't connect. Is Go MessagePasser up?")
		break
	
	#Close the connection, but commented because we don't want to do that yet.
	#MessagePasser.close()

## Build and Send Message
## # this function builds and sends a message
def sendMessage(src, dest, content, kind):
	message = src + DELIMITER + dest + DELIMITER + content + DELIMITER + kind
	MessagePasser.send(message)
	receivedData = MessagePasser.recv(BUFFER_SIZE)
	return receivedData