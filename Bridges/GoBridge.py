###########################################################
#Multegula - GoBridge.py                                  #
#Functions to create local socket and messages            #
#Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He#
###########################################################

import socket
import time #Needed for labeling date/time
import datetime #Needed for labeling date/time
import base64 #Needed for encoding network messages

########PARAMETERS########
#Set arbitrary buffer size for received messages
BUFFER_SIZE = 200
DELIMITER = "##"
LOCALHOST_IP = '127.0.0.1'
TCP_PORT = 44444
##########################


## RUN the GoBridge
## # this function starts the GoBridge running
def runGoBridge():
	#Get Time
	timestamp = int(time.time())
	prettytime = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
	
	#Set up the connection
	GoBridge = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		#Try to open connection to local Go Bridge
		GoBridge.connect((LOCALHOST_IP, TCP_PORT))
	except:
		print("[" + prettytime + "] Can't connect. Is GoBridge up?")

	###############FOR TESTING/DEBUG ONLY#################
	message = "localhost##localhost##messagecontent##testMessage"
	GoBridge.send(message.encode(encoding='utf-8'))
	###############FOR TESTING/DEBUG ONLY#################
	
	#Close the connection, but commented because we don't want to do that yet.
	#MessagePasser.close()

## Build and Send Message
## # this function builds and sends a message.
## # Base64 encoding isn't my favorite, but it became necessary in Python 3.
def sendMessage(src, dest, content, kind, multicastFlag):
	message = src + DELIMITER + dest + DELIMITER + content + DELIMITER + kind + DELIMITER + multicastFlag
	GoBridge.send(message.encode(encoding='utf-8'))

## Receive Message
## # this function receives a message from the receive buffer
def receiveMessage():
	receivedData = GoBridge.recv(BUFFER_SIZE)
	return receivedData
