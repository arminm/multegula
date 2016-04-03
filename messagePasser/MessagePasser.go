////////////////////////////////////////////////////////////
//Multegula - MessagePasser.go
//Multicasting Message Passer for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package messagePasser

import (
	"encoding/json"
	"os"
	"fmt"
	"net"
	"bufio"
	"strings"
	"sync"
	"time"
)

/* DNS Configuration */
type Configuration struct {
    BootstrapServer []string //BootstrapServer DNS
    LocalName []string // Local DNS
    Group []string // Group DNS
}

/* delimiter for formatting message */
/* NOTE: Make sure a message does not include the delimiter in any of
 *       the fields.
 */
const delimiter string = "##"

/* message structure
 * before message transported through TCP connection, it will
 * be converted to string in the format of: Source##Destination##Content##Kind
 * when message is received, it will be reconstructed
 **/
type Message struct {
	Source string // the DNS name of sending node
	Destination string // the DNS name of receiving node
	Content string // the Content of message
	Kind string // the Kind of messages
}

/* InitMessagePasser has to wait all work done before exiting */
var wg sync.WaitGroup

/*
 * convert message to string
 * @param	message
 *			message to be converted
 *
 * @return	the string format of the message
 **/
func encodeMessage(message Message) string {
	return message.Source + delimiter + message.Destination + delimiter + message.Content + delimiter + message.Kind
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
	return Message{Source: elements[0], Destination: elements[1], Content: elements[2],	Kind: elements[3]}
}

/* map stores connections to each node
 * <key, value> = <dns, connection>
 **/
var connections map[string]net.Conn = make(map[string]net.Conn)

/*
 * connection for localhost, this is the receive side,
 * the send side is stored in connections map
 **/
var localConn net.Conn

/* the queue for messages to be sent */
var sendQueue chan Message = make(chan Message, 100)

/* the queue for received messages */
var receivedQueue chan Message = make(chan Message, 100)

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
		} else if (dns > localName) {
			latterNodes[dns] = true
        } else {
            frontNodes[dns] = true
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
 *
 * @param   localName
 *          the DNS name of local node
 **/
func acceptConnection(frontNodes map[string]bool, localName string) {
    defer wg.Done()
    ln, _ := net.Listen("tcp", port)
	for len(frontNodes) > 0 {
		/*
		 * when a node first connects to other nodes, it will first
		 * send it's DNS name so that another node can know it's name
		 **/
		conn, _ := ln.Accept()
		dns, _ := bufio.NewReader(conn).ReadString('\n')
        /* dns contains \n in it's end */
        delete(frontNodes, dns[0:len(dns) - 1])
        if(dns[0:len(dns) - 1] == localName) {
            localConn = conn
        } else {
            connections[dns[0:len(dns) - 1]] = conn
        }
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
func sendConnection(latterNodes map[string]bool, localName string) {
    defer wg.Done()
	for key, _ := range latterNodes {
		conn, err := net.Dial("tcp", key + port)
        for err != nil {
            fmt.Print(".")
            time.Sleep(time.Second * 1)
            conn, err = net.Dial("tcp", key + port)
        }
		/* send local DNS to other side of the connection */
		conn.Write([]byte(localName + "\n"))
		connections[key] = conn
	}
    fmt.Println()
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
    	receivedQueue <- decodeMessage(messageString[0:len(messageString) - 1])
		}
	}
}

/*
 * for each TCP connection, start a new receiveMessageFromConn routine to
 * receive messages sent from that connection. A constraint for this mechanism
 * is that each routine waits in a infinite loop which makes code inefficient.
 **/
func startReceiveRoutine() {
	for _, conn := range connections {
		go receiveMessageFromConn(conn)
	}
    go receiveMessageFromConn(localConn)
}

/*
 * whnever there are messages in sendQueue, send it out to TCP connection
 **/
func sendMessageToConn() {
	for {
		message := <- sendQueue
		connections[message.Destination].Write([]byte(encodeMessage(message) + "\n"))
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
 *			in receivedQueue; otherwise, return an empty message
 **/
func Receive() Message {
    var message Message = Message{}
	if(len(receivedQueue) > 0){
		message = <- receivedQueue
	}
	return message
}

/* 
 * receive message, this is a public method and it will be blocked if there is 
 * no message can be received right now
 * @return	if there are receivable messages in receivedQueue, return the first
 *			in receivedQueue; otherwise, return an empty message
 **/
func BlockReceive() Message {
	message := <- receivedQueue
	return message
}

/*
 * initialize MessagePasser, this is a public method
 **/
func InitMessagePasser() {
	file, _ := os.Open("./messagePasser/config.json")
	decoder := json.NewDecoder(file)
	configuration := Configuration{}
	err := decoder.Decode(&configuration)
	if err != nil {
	  fmt.Println("error:", err)
	}

    /* separate DNS names */
	frontNodes, latterNodes := getFrontAndLatterNodes(configuration.Group, configuration.LocalName[0])

    /* wait for connections setup before proceeding */
    wg.Add(2)
	/* setup TCP connections */
	go acceptConnection(frontNodes, configuration.LocalName[0])
	go sendConnection(latterNodes, configuration.LocalName[0])
    wg.Wait()

	/* start routines listening on each connection to receive messages */
	startReceiveRoutine()

  	/* start routine to send message */
  	go sendMessageToConn()
}
