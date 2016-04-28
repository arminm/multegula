###########################################################
#Multegula - GoBridge.py                                  #
#Functions to create local socket and messages            #
#Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He#
###########################################################

#######IMPORTS#######
import socket #Needed for network communications
import time #Needed for labeling date/time
import datetime #Needed for labeling date/time
import queue #Needed for receive queue
import sys #Needed to exit
from UI.typedefs import *
#####################

# GoBridge class
class GoBridge :
    ### __init___ - initialize and return GoBridge
    ## # this function starts the GoBridge running
	## # Returns a connected socket object GoBridge
	def __init__(self, CLI_PORT, src = DEFAULT_SRC) :
		# set the self src
		self.src = src;
		
		#Set up the connection
		GoSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		#Disable Nagle's Algorithm to decrease latency.
		#TCP_NODELAY sends packets immediately.
		GoSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		
		try:
			#Try to open connection to local Go Bridge
			print("Attempting to connect to local Go bridge on port " + CLI_PORT)
			GoSocket.connect((LOCALHOST_IP, int(CLI_PORT)))
		except Exception as e:
			#NOTE: this is mostly useful for debugging, but in reality the game couldn't run without this.
			print(e)
			print(self.getPrettyTime() + " Can't connect. Is PyBridge up?")
			sys.exit(1)

		#And declare GoBridge
		self.GoSocket = GoSocket

		#Establish a queue for received messages
		self.receiveQueue = queue.Queue()

	## Get Pretty Time
	## # Get pretty time for printing in error logs.
	def getPrettyTime(self): 
		#Get Time
		timestamp = int(time.time())
		prettytime = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
		return 	'[' + prettytime + ']'
			
	## Build and Send Message
	## # this function builds and sends a message.
	## # Explicit encoding declaration became necessary in Python 3.
	def sendMessage(self, pyMessage):
		if pyMessage.src == DEFAULT_SRC:
			print('GoBridge: ' + self.getPrettyTime() + ' Source name not set. Cannot send message.')
		else:
			# determine if this is a multicast message
			if(pyMessage.multicast == True):
				pyMessage.dest = MULTICAST_DEST
			else:
				pyMessage.dest = pyMessage.src	

			# assemble the string version of the message
			toSend = pyMessage.assemble()

			try:	
				self.GoSocket.send(toSend.encode(encoding='utf-8'))
			except: 
				print('GoBridge: ' + self.getPrettyTime() + ' Error sending on GoSocket:')
				print('   ' + toSend);

	## Receive Thread
	## # this function receives a message from the receive buffer
	## # and adds it to a receive queue for pickup by other functions.
	def receiveThread(self):
		while True:
			receivedData = self.GoSocket.recv(BUFFER_SIZE)
			if receivedData:
				# remove header and footer of the received data
				transform = str(receivedData).replace("b'", "")
				transform = transform.replace("'", "")

				# split multiple messages up if more than one was recieved
				receivedMessages = str(transform).split('\\n')

				# put all messages into the recieved queue
				for message in receivedMessages:
					if message :
						self.receiveQueue.put(message)

	## Receive Message
	## # this function pulls a message from the receive queue
	def receiveMessage(self):
		message = PyMessage()
		# only try and get a message if there is something in the queue.
		if not(self.receiveQueue.empty()):
			received = self.receiveQueue.get()
			message.crack(received)
			self.receiveQueue.task_done()

		return message

