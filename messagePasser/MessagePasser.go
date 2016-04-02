////////////////////////////////////////////////////////////
//Multegula - MessagePasser.go
//Multicasting Message Passer for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package messagePasser

import (
	"bufio"
	"encoding/json"
	"errors"
	"fmt"
	"net"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

type Node struct {
	Name string
	IP   string
	Port int
	DNS  string
}

/* DNS Configuration */
type Configuration struct {
	BootstrapServer []string //BootstrapServer DNS
	LocalName       []string // Local DNS
	Group           []string // Group DNS
	Nodes           []Node
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
	Source      string // the DNS name of sending node
	Destination string // the DNS name of receiving node
	Content     string // the Content of message
	Kind        string // the Kind of messages
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
	return Message{Source: elements[0], Destination: elements[1], Content: elements[2], Kind: elements[3]}
}

/*
 * local instance holding the parsed config info.
 */
var config Configuration = Configuration{}

func Config() Configuration {
	return config
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

/*
 * The local node's information.
 */
var localNode Node

/* the queue for messages to be sent */
var sendQueue chan Message = make(chan Message, 100)

/* the queue for received messages */
var receivedQueue chan Message = make(chan Message, 100)

/* port number for TCP connection */
const port string = ":8081"

func findNodeByName(nodes []Node, name string) (Node, error) {
	for _, node := range nodes {
		if node.Name == name {
			return node, nil
		}
	}
	return Node{}, errors.New("Node not found: " + name)
}

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
func getFrontAndLatterNodes(nodes []Node, localNode Node) (map[string]Node, map[string]Node) {
	var frontNodes map[string]Node = make(map[string]Node)
	var latterNodes map[string]Node = make(map[string]Node)
	for _, node := range nodes {
		if node.Name < localNode.Name {
			frontNodes[node.Name] = node
		} else if node.Name > localNode.Name {
			latterNodes[node.Name] = node
		} else {
			frontNodes[node.Name] = node
			latterNodes[node.Name] = node
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
func acceptConnection(frontNodes map[string]Node, localNode Node) {
	defer wg.Done()
	fmt.Println("Local Port:", strconv.Itoa(localNode.Port))
	ln, err := net.Listen("tcp", ":"+strconv.Itoa(localNode.Port))
	if err != nil {
		fmt.Println("Couldn't Start Server...")
		panic(err)
	}
	for len(frontNodes) > 0 {
		/*
		 * when a node first connects to other nodes, it will first
		 * send it's DNS name so that another node can know it's name
		 **/
		conn, _ := ln.Accept()
		dns, _ := bufio.NewReader(conn).ReadString('\n')
		dns = dns[0 : len(dns)-1]
		/* dns contains \n in it's end */
		delete(frontNodes, dns)
		if dns == localNode.Name {
			localConn = conn
		} else {
			connections[dns] = conn
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
func sendConnection(latterNodes map[string]Node, localNode Node) {
	defer wg.Done()
	for _, node := range latterNodes {
		conn, err := net.Dial("tcp", node.IP+":"+strconv.Itoa(node.Port))
		for err != nil {
			fmt.Print(".")
			time.Sleep(time.Second * 1)
			conn, err = net.Dial("tcp", node.IP+":"+strconv.Itoa(node.Port))
		}
		/* send local DNS to other side of the connection */
		conn.Write([]byte(localNode.Name + "\n"))
		connections[node.Name] = conn
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
		if len(messageString) > 0 {
			receivedQueue <- decodeMessage(messageString[0 : len(messageString)-1])
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
		message := <-sendQueue
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
	if len(receivedQueue) > 0 {
		message = <-receivedQueue
	}
	return message
}

/*
 * initialize MessagePasser, this is a public method
 **/
func InitMessagePasser(configName string, localName string) {
	file, _ := os.Open("./messagePasser/" + configName + ".json")
	decoder := json.NewDecoder(file)
	err := decoder.Decode(&config)
	if err != nil {
		fmt.Println("error:", err)
	}
	// fmt.Println("Configuration:", config)
	localNode, err := findNodeByName(config.Nodes, localName)
	if err != nil {
		panic(err)
	}
	/* separate DNS names */
	frontNodes, latterNodes := getFrontAndLatterNodes(config.Nodes, localNode)

	/* wait for connections setup before proceeding */
	wg.Add(2)
	/* setup TCP connections */
	go acceptConnection(frontNodes, localNode)
	go sendConnection(latterNodes, localNode)
	wg.Wait()

	/* start routines listening on each connection to receive messages */
	startReceiveRoutine()

	/* start routine to send message */
	go sendMessageToConn()
}
