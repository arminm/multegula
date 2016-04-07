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

# GoBridge class
class GoBridge :
    ### __init___ - initialize and return GoBridge
    ## # this function starts the GoBridge running
	## # Returns a connected socket object GoBridge
	def __init__(self, src) :
		# set the 
		self.src = src;

		#Get Time
		timestamp = int(time.time())
		prettytime = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
		
		#Set up the connection
		GoSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		#Disable Nagle's Algorithm to decrease latency.
		#TCP_NODELAY sends packets immediately.
		GoSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		
		try:
			#Try to open connection to local Go Bridge
			GoSocket.connect((LOCALHOST_IP, TCP_PORT))
		except:
			#NOTE: this is mostly useful for debugging, but in reality the game couldn't run without this.
			print("[" + prettytime + "] Can't connect. Is GoBridge up?")

		#And declare GoBridge
		self.GoSocket = GoSocket

	## Build and Send Message
	## # this function builds and sends a message.
	## # Explicit encoding declaration became necessary in Python 3.
	def sendMessage(self, src, dest, content, kind ):
		message = src + DELIMITER + dest + DELIMITER + content + DELIMITER + kind
		try:	
			self.GoSocket.send(message.encode(encoding='utf-8'))
		except: 
			timestamp = int(time.time())
			prettytime = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
			print("[" + prettytime + "] Error sending on GoSocket:")
			print("\t" + message);

	## Receive Message
	## # this function receives a message from the receive buffer
	def receiveMessage():
		receivedData = self.GoSocket.recv(BUFFER_SIZE)
		return receivedData

	def multicast(self, content, kind):
		self.sendMessage(self.src, "ER'BODY", content, kind)
