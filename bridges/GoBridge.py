###########################################################
#Multegula - GoBridge.py                                  #
#Functions to create local socket and messages            #
#Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He#
###########################################################

#######IMPORTS#######
import socket #Needed for network communications
import time #Needed for labeling date/time
import datetime #Needed for labeling date/time
import base64 #Needed for encoding network messages
#####################

########PARAMETERS########
BUFFER_SIZE = 200 #Arbitrary buffer size for received messages
DELIMITER = "##"
LOCALHOST_IP = '127.0.0.1'
TCP_PORT = 44444
##########################

# BALL class
class GoBridge :
    ### __init___ - initialize and return GoBridge
    ## # this function starts the GoBridge running
	## # Returns a connected socket object GoBridge
	def __init__(self) :
		#Get Time
		timestamp = int(time.time())
		prettytime = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
		
		#Set up the connection
		GoBridge = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		#Disable Nagle's Algorithm to decrease latency.
		#TCP_NODELAY sends packets immediately.
		GoBridge.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		
		try:
			#Try to open connection to local Go Bridge
			GoBridge.connect((LOCALHOST_IP, TCP_PORT))
		except:
			print("[" + prettytime + "] Can't connect. Is GoBridge up?")

		#And declare GoBridge
		self.GoBridge = GoBridge

	## Build and Send Message
	## # this function builds and sends a message.
	## # Explicit encoding declaration became necessary in Python 3.
	def sendMessage(src, dest, content, kind, multicastFlag):
		message = src + DELIMITER + dest + DELIMITER + content + DELIMITER + kind + DELIMITER + multicastFlag
		GoBridge.send(message.encode(encoding='utf-8'))

	## Receive Message
	## # this function receives a message from the receive buffer
	def receiveMessage():
		receivedData = GoBridge.recv(BUFFER_SIZE)
		return receivedData