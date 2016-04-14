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
#####################

########PARAMETERS########
BUFFER_SIZE = 200 #Arbitrary buffer size for received messages
DELIMITER = '##'
PAYLOAD_DELIMITER = '|'
LOCALHOST_IP = 'localhost'
DEFAULT_SRC = 'UNSET'
MULTICAST_DEST = 'EVERYBODY'
MULTEGULA_DEST = 'MULTEGULA'
DEFAULT_PORT = 44444
##########################

# PyMessage class 
class PyMessage :
	### __init__ - initialize and return an empty PyMessage
	def __init__(self):
		self.kind = ''
		self.src = ''
		self.dest = ''
		self.content = None
		self.multicast = False

	### crack - crack a PyMessage from the the 'received' string
	def crack(self, received):
		receivedArray = str(received).split(DELIMITER)
		self.src = receivedArray[0].replace("b'", '')
		self.dest = receivedArray[1]
		self.content = receivedArray[2].split(PAYLOAD_DELIMITER)
		self.kind = receivedArray[3].replace("\\n'", '')

	### assemble - assemble the message and return
	def assemble(self):
		return self.src + DELIMITER + self.dest + DELIMITER + self.content + DELIMITER + self.kind + '\n'

	### toString - return a visually appealing string relective of the contents in the message
	def toString(self):
		return 'source: ' + self.src + ', type: ' + self.kind + ', content: ' + str(self.content)

# GoBridge class
class GoBridge :
    ### __init___ - initialize and return GoBridge
    ## # this function starts the GoBridge running
	## # Returns a connected socket object GoBridge
	def __init__(self, CLI_PORT, src = DEFAULT_SRC,) :
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
				pyMessage.dest = MULTEGULA_DEST	

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
			if not receivedData:
				pass
			else:
				self.receiveQueue.put(receivedData)


	## Receive Message
	## # this function pulls a message from the receive queue
	def receiveMessage(self):
		message = PyMessage()
		# only try and get a message if there is something in the queue.
		if not(self.receiveQueue.empty()):
			## TODO: Eventually put this in a try/except
			received = self.receiveQueue.get()
			message.crack(received)
			self.receiveQueue.task_done()

		return message

