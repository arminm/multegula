////////////////////////////////////////////////////////////
//Multegula - MessagePasser.go 
//Multicasting Message Passer for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package main

import (
	"encoding/json"
	"os"
	"fmt"
	"net"
	"bufio"
	"strings"
)

//Config Reading Example
type Configuration struct {
    bootstrapServer  []string
    localName []string
    group []string
}

/* delimiter for formatting message */
const delimiter string = "##"

/* message structure
 * before message transported through TCP connection, it will
 * be converted to string in the format of: source##destination##content##kind
 # when message is received, it will be reconstructed
 **/
type Message struct {
	source string // the DNS name of sending node
	destination string // the DNS name of receiving node
	content string // the content of message
	kind string //s the kind of messages
}

/* 
 * convert message to string
 * @param	message
 *			message to be converted
 *
 * @return	the string format of the message
 **/
func encodeMessage(message Message) string {
	return message.source + delimiter + message.destination + delimiter + message.content + delimiter + message.kind
}

/*
 * construct message from it's string format
 * @param	messageString
 *			message in string format
 *
 * @return	message
 **/
func decodeMessage(messageString string) Message {
	var elements []string = strings.Split(messageString, delimiter)
	return Message{
		source: elements[0],
		destination: elements[1],
		content: elements[2],
		kind: elements[3]
	}
}

/* map stores connections to each node
 * <key, value> = <dns, connection>
 **/
var connections map[string]Conn = make(map[string]Conn)

/* the queue for messages to be sent */
var sendQueue chan = make(chan Message, 100)

/* the queue for received messages */
var receivedQueue chan = make(chan Message, 100)

/* port number for TCP connection */
const port string = ":8081"

/*
 * separate nodes' DNS name into two parts based on lexicographical order
 * @param	group
 *			the DNS name of each node in the group
 *
 * @param	localName
 *			the DNS name of local node
 * 
 * @return	frontNodes
 *			nodes smaller than localName
 *			latterNodes
 *			nodes greater or equal to localName
 **/
func getFrontAndLatterNodes(group []string, localName string) (map[string]bool, map[string]bool) {
	var frontNodes map[string]bool = make(map[string]bool)
	var latterNodes map[string]bool = make(map[string]bool)
	for _, dns := range group {
		if(dns < localName) {
			frontNodes[dns] = true
		} else {
			latterNodes[dns] = true
		}
	}
	return frontNodes, latterNodes
}


/* 
 * accepts connections from other nodes and stores 
 * connections into connections map, after accepting
 * all connections from all other nodes in the group,
 * this routine exits
 * @param	frontNodes
 *			map that contains all nodes with smaller DNS names
 **/
func acceptConnection(frontNodes map[string]bool) {
	fmt.Println("Accepting connections...")
	ln, _ = net.Listen("tcp", port)
	for len(frontNodes) > 0 {
		/* 
		 * when a node first connects to other nodes, it will first 
		 * send it's DNS name so that another node can know it's name
		 **/
		conn, _ := ln.Accept()
		dns, _ := bufio.NewReader(conn).ReadString('\n')
		fmt.Println("Received connection from " + dns)
		delete(frontNodes, dns)
		connections[dns] = conn
	}
}

/*
 * send connections to nodes with greater DNS names
 * and stores connections into connections map
 * @param	latterNodes
 *			map that contains all nodes with greater or equal DNS names
 *
 * @param	localName
 *			the DNS name of local node
 **/
func sendConnection(latterNodes map[string]bool, string localName) {
	for key, value := range latterNodes {
		conn, _ := net.Dial("tcp", key + port)
		/* send local DNS to other side of the connection */
		conn.Write([]byte(key + "\n"))
		connections[key] = conn
	}
}

/* 
 * receive message from TCP connection, reconstruct message and 
 * put it into receivedQueue of message
 * @param	conn
 *			TCP connection
 **/
func receiveMessageFromConn(conn net.Conn) {
	for {
		messageString, _ := bufio.NewReader(conn).ReadString('\n')
		if(len(messageString) > 0) {
			receivedQueue <- decodeMessage(messageString)
		}
	}
}

/* 
 * for each TCP connection, start a new receiveMessageFromConn routine to
 * receive messages sent from that connection. A constraint for this mechanism
 * is that each routine waits in a infinite loop which makes code inefficient.
 * //TODO find more efficient way in go for listening messages for net.Conn
 **/
func startReceiveRoutine() {
	for dns, conn := range connections {
		go receiveMessageFromConn(conn)
	}
}

/*
 * whenever there are messages in sendQueue, send it out to TCP connection
 **/
func sendMessageToConn() {
	for {
		message := <- sendQueue
		conn := connections[message.destination]
		conn.Write([]byte(encodeMessage(message) + "\n"))
	}
}

/* 
 * put message to sendQueue, since the chan <- maybe blocked if the channel is full,
 * in order to not block the void send(message Message) method, we creates a new routine
 * to do this
 * @param	message
 *			the message to be put into sendQueue
 **/
func putMessageToSendQueue(message Message) {
	sendQueue <- message
}

/* 
 * send message, this is a public method
 * @param	message
 *			message to be sent
 **/
func Send(message Message) {
	go putMessageToSendQueue(message)
}

/* 
 * receive message, this is a public method
 * @return	if there are receivable messages in receivedQueue, return the first
 *			in receivedQueue; otherwise, return nil
 **/
func Receive() Message {
	var message Message = nil
	if(len(receivedQueue) > 0){
		message = <- receivedQueue
	}
	return message
}

func main() {
	file, _ := os.Open("config.json")
	decoder := json.NewDecoder(file)
	configuration := Configuration{}
	err := decoder.Decode(&configuration)
	if err != nil {
	  fmt.Println("error:", err)
	}

	/* separate DNS names */
	frontNodes, latterNodes := getFrontAndLatterNodes(configuration.group, configuration.localName[0])

	/* setup TCP connections */
	acceptConnection(frontNodes)
	sendConnection(latterNodes, configuration.localName[0])

	/* start routines listening on each connection to receive messages */
	startReceiveRoutine()

  	/* start routine to send message */
  	go sendMessageToConn()
}
