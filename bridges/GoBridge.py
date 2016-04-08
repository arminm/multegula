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
#####################

########PARAMETERS########
BUFFER_SIZE = 200 #Arbitrary buffer size for received messages
DELIMITER = "##"
LOCALHOST_IP = 'localhost'
DEFAULT_SRC = 'UNSET'
MULTICAST_DEST = "EVERYBODY"
TCP_PORT = 44444
##########################

# GoBridge class
class GoBridge :
    ### __init___ - initialize and return GoBridge
    ## # this function starts the GoBridge running
	## # Returns a connected socket object GoBridge
	def __init__(self, src = DEFAULT_SRC) :
		# set the self src
		self.src = src;
		
		#Set up the connection
		GoSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		#Disable Nagle's Algorithm to decrease latency.
		#TCP_NODELAY sends packets immediately.
		GoSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		#Disable blocking so our receive thread can continue.
		#Currently blocking - I think this is okay. -Garrett
		#GoSocket.setblocking(0)
		
		try:
			#Try to open connection to local Go Bridge
			GoSocket.connect((LOCALHOST_IP, TCP_PORT))
		except:
			#NOTE: this is mostly useful for debugging, but in reality the game couldn't run without this.
			print(self.getPrettyTime() + " Can't connect. Is GoBridge up?")

		#And declare GoBridge
		self.GoSocket = GoSocket

		#Establish a queue for received messages
		self.q = queue.Queue()

	## Get Pretty Time
	## # Get pretty time for printing in error logs.
	def getPrettyTime(self): 
		#Get Time
		timestamp = int(time.time())
		prettytime = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
		return 	"[" + prettytime + "]"
			
	## Build and Send Message
	## # this function builds and sends a message.
	## # Explicit encoding declaration became necessary in Python 3.
	def sendMessage(self, src, dest, content, kind):
		if self.src == DEFAULT_SRC:
			print(self.getPrettyTime() + " Source name not set. Cannot send message.")
		else:
			message = src + DELIMITER + dest + DELIMITER + content + DELIMITER + kind + "\n"
			try:	
				self.GoSocket.send(message.encode(encoding='utf-8'))
			except: 
				print(self.getPrettyTime() + " Error sending on GoSocket:")
				print("\t" + message);

	## Multicast Message
	## # This function is used to multicast a message, call when we want
	## # a message multicasted versus a regular send.
	def multicast(self, content, kind):
		self.sendMessage(self.src, MULTICAST_DEST, content, kind)

	## Receive Thread
	## # this function receives a message from the receive buffer
	## # and adds it to a receive queue for pickup by other functions.
	## # CURRENTLY BLOCKS, SO ITERATOR DOES NOT WORK - I think this is okay. -Garrett
	def receiveThread(self):
		i = 0;
		while True:
			print(i)
			i += 1
			receivedData = self.GoSocket.recv(BUFFER_SIZE)
			if not receivedData:
				break
			self.q.put(receivedData)

	## Receive Message
	## # this function pulls a message from the receive queue
	def receiveMessage(self):
		message = self.q.get()
		#Lets Python know that work on this element is done.
		self.q.task_done()
		return message
