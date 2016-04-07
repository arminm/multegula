////////////////////////////////////////////////////////////
//Multegula - MessagePasser.go
//Multicasting Message Passer for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package messagePasser

import (
	"encoding/gob"
	"encoding/json"
	"errors"
	"fmt"
	"net"
	"os"
	"strconv"
	"sync"
	"time"
)

// Constants
const KIND_MULTICAST string = "multicast"
const KIND_REMULTICAST string = "remulticast"

/* the size of queue: sendQueue, receivedQueue,
 * sendDelayedQueue and receiveDelayedQueue
 **/
const QUEUE_SIZE int = 100

// Node structure to hold each node's information
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
	Nodes           []Node   // List of available nodes
}

/* Message structure
 * before message transported through TCP connection, it will
 * be converted to string in the format of: Source##Destination##Content##Kind
 * when message is received, it will be reconstructed
 **/
type Message struct {
	Source      string // the DNS name of sending node
	Destination string // the DNS name of receiving node
	Content     string // the Content of message
	Kind        string // the Kind of messages
	SeqNum      int
}

/* InitMessagePasser has to wait for all work to be done before exiting */
var wg sync.WaitGroup

func updateSeqNum(message *Message) {
	seqNum := seqNums[message.Destination] + 1
	seqNums[message.Destination] = seqNum
	message.SeqNum = seqNum
}

/*
 * send TCP messages
 * @param	conn – connection to send message over
 * @param	message – message to be sent
 **/
func sendMessageTCP(nodeName string, message *Message) {
	encoder := gob.NewEncoder(connections[nodeName])
	encoder.Encode(message)
}

/*
 * receive TCP messages
 * @param	conn – the connection to use
 *
 * @return	message
 **/
func receiveMessageTCP(conn net.Conn) Message {
	dec := gob.NewDecoder(conn)
	msg := &Message{}
	dec.Decode(msg)
	// fmt.Printf("Received : %+v\n", msg)
	return *msg
}

/*
 * basic multicasts a message to all nodes
 */
func Multicast(message *Message) {
	if len(message.Destination) == 0 {
		message.Destination = config.Group[0]
	}
	if message.Kind != KIND_REMULTICAST {
		message.Kind = KIND_MULTICAST
		updateSeqNum(message)
	}

	for _, node := range config.Nodes {
		sendMessageTCP(node.Name, message)
	}
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
var seqNums map[string]int = make(map[string]int)

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
var sendQueue chan Message = make(chan Message, QUEUE_SIZE)

/* the queue for received messages */
var receivedQueue chan Message = make(chan Message, QUEUE_SIZE)

/*
 * finds a node within an array of nodes by Name
 */
func FindNodeByName(nodes []Node, name string) (Node, error) {
	for _, node := range nodes {
		if node.Name == name {
			return node, nil
		}
	}
	return Node{}, errors.New("Node not found: " + name)
}

/*
 * separate nodes' DNS name into two parts based on lexicographical order
 * @param	nodes
 *			the nodes in the group
 *
 * @param	localNode
 *
 * @return	frontNodes – nodes smaller than localName
 *					latterNodes – nodes greater or equal to localName
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
 *			map that contains all nodes with smaller Node names
 *
 * @param   localNode
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
		msg := receiveMessageTCP(conn)
		// remove the connected node from the frontNodes
		delete(frontNodes, msg.Source)
		if msg.Source == localNode.Name {
			localConn = conn
		} else {
			connections[msg.Source] = conn
			seqNums[msg.Source] = 0
		}
	}
}

/*
 * send connections to nodes with greater Names
 * and stores connections into connections map
 * @param	latterNodes
 *			map that contains all nodes with greater or equal Node names
 *
 * @param	localNode
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
		connections[node.Name] = conn
		seqNums[node.Name] = 0

		/* send an initial ping message to other side of the connection */
		msg := Message{localNode.Name, node.Name, "ping", "ping", 0}
		sendMessageTCP(node.Name, &msg)
	}
	fmt.Println()
}

/*
 * put message to receiveQueue, since the chan <- maybe blocked if the channel is full,
 * in order to not block the void receiveMessageFromConn(conn) method, we creates a new routine
 * to do this
 * @param	message
 *			the message to be put into receiveQueue
 **/
func putMessageToReceivedQueue(message Message) {
	receivedQueue <- message
}

/*
 * receive message from TCP connection, and put it into receivedQueue of message
 * @param	conn
 *			TCP connection
 **/
func receiveMessageFromConn(conn net.Conn) {
	for {
		msg := receiveMessageTCP(conn)
		// if msg.Kind == KIND_MULTICAST {
		// 	msg.Kind = KIND_REMULTICAST
		// 	Multicast(&msg)
		// }
		rule := matchReceiveRule(msg)
		/* no rule matched, put it into receivedQueue */
		if (rule == Rule{}) {
			go putMessageToReceivedQueue(msg)
			/*
			 * there are delayed messages in receiveDelayedQueue
			 * get one and put it into receivedQueue
			 */
			if len(receiveDelayedQueue) > 0 {
				delayedMessage := <-receiveDelayedQueue
				go putMessageToReceivedQueue(delayedMessage)
			}
		} else {
			/*
			 * there is a receive rule matched, we only need to
			 * check "delay" rule, since other rule will drop
			 * this message
			 */
			if rule.Kind == "delay" {
				go putMessageToReceiveDelayedQueue(msg)
			}
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
		rule := matchSendRule(message)
		/* no rules matched, send the message */
		if (rule == Rule{}) {
			sendMessageTCP(message.Destination, &message)
			/* there are delayed messages, send one */
			if len(sendDelayedQueue) > 0 {
				delayedMessage := <-sendDelayedQueue
				sendMessageTCP(delayedMessage.Destination, &delayedMessage)
			}
		} else {
			/*
			 * rule matched, only check delay rule, because other rules
			 * will drop this message
			 */
			if rule.Kind == "delay" {
				go putMessageToSendDelayedQueue(message)
			}
		}
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
	updateSeqNum(&message)
	go putMessageToSendQueue(message)
}

/*
 * Delivers received messages from the receiveQueue
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
 * receive message, this is a public method and it will be blocked if there is
 * no message can be received right now
 * @return	if there are receivable messages in receivedQueue, return the first
 *			in receivedQueue; otherwise, return an empty message
 **/
func BlockReceive() Message {
	message := <-receivedQueue
	return message
}

/*
 * initialize MessagePasser, this is a public method
 **/
func InitMessagePasser(configName string, localName string) {
	//filePath := "./messagePasser/" + configName + ".json"
	file, _ := os.Open(configName)
	decoder := json.NewDecoder(file)
	err := decoder.Decode(&config)
    
	if err != nil {
		fmt.Println("error:", err)
	}
	localNode, err := FindNodeByName(config.Nodes, localName)
	if err != nil {
		panic(err)
	}
	/* keep track of group seqNum for multicasting */
	seqNums[config.Group[0]] = 0

	/* separate Node names */
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
