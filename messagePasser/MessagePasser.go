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
var sendChannel chan Message = make(chan Message, 100)

/* the queue for received messages */
var receiveChannel chan Message = make(chan Message, 100)
var receiveQueue []Message = make([]Message, 10, 10)

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
	receiveChannel <- message
}

/*
 * receive message from TCP connection, and put it into receivedQueue of message
 * @param	conn
 *			TCP connection
 **/
func receiveMessageFromConn(conn net.Conn) {
	for {
		msg := receiveMessageTCP(conn)
		if msg.Kind == KIND_MULTICAST {
			msg.Kind = KIND_REMULTICAST
			go Multicast(&msg)
		}
		rule := matchReceiveRule(msg)
		/* no rule matched, put it into receivedQueue */
		if (rule == Rule{}) {
			go putMessageToReceivedQueue(msg)
			/*
			 * there are delayed messages in receiveDelayedQueue
			 * get one and put it into receivedQueue
			 */
			for len(receiveDelayedQueue) > 0 {
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
 * whnever there are messages in sendChannel, send it out to TCP connection
 **/
func sendMessageToConn() {
	for {
		message := <-sendChannel
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
 * put message to sendChannel, since the chan <- maybe blocked if the channel is full,
 * in order to not block the void send(message Message) method, we creates a new routine
 * to do this
 * @param	message
 *			the message to be put into sendChannel
 **/
func putMessageToSendQueue(message Message) {
	sendChannel <- message
}

/*
 * send message, this is a public method
 * @param	message
 *			message to be sent
 **/
func Send(message Message) {
    if(message == Message{}) {
        fmt.Println("Empty message, it is dropped!")
    } else {
        if _, ok := connections[message.Destination]; ok {
    	    updateSeqNum(&message)
        	go putMessageToSendQueue(message)
        } else {
            fmt.Printf("Message's destination %s is not found, it is dropped!\n", message.Destination)
        }
    }
}

/*
 * Delivers received messages from the receiveQueue
 * @return	if there are receivable messages in receiveQueue, return the first
 *			in receiveQueue; otherwise, return an empty message
 **/
func Receive() Message {
	return Pop(&receiveQueue)
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
/*
 * Receives a message from the receive channel and inserts it into the queue.
 */
func receiveQueueRoutine() {
	for {
		message := <-receiveChannel
		for i, msg := range receiveQueue {
			if msg.Source == message.Source {
				if msg.SeqNum == message.SeqNum {
					break
				} else if msg.SeqNum > message.SeqNum {
					receiveQueue = *Insert(&receiveQueue, message, i)
					break
				}
			} else if i == len(receiveQueue) {
				Push(&receiveQueue, message)
				break
			}
		}
	}
}

/*
 * Prompts the user for the configuration file's name
 * @return configuration file's name string
 */
func getConfigName() string {
	var configName string
	fmt.Println("What's the config file's name? (ex. config)")
	fmt.Scanf("%s", &configName)
	if len(configName) == 0 {
		configName = "config" // default name
	}
	return configName
}

/*
 * Prompts the user for the local Node's name
 * @return local Node's name string
 */
func getLocalName() string {
	var localName string
	fmt.Println("Who are you? (ex. armin)")
	fmt.Scanf("%s", &localName)
	if len(localName) == 0 {
		localName = "unknown" // default name
	}
	return localName
}

/*
 * open config file
 * @param configName the name of config file
 * @return the handler of config file
 */
 func openConfigFile(configName string) *os.File {
	filePath := "./messagePasser/" + configName + ".json"
    file, err := os.Open(filePath)
    for err != nil {
        fmt.Println("Error: cannot find or open the config file, please set config file again.")
        configName = getConfigName()
        filePath = "./messagePasser/" + configName + ".json"
        file, err = os.Open(filePath)
    }
    return file
 }

 /*
  * decode the config file
  * @param configName the name of config file
  */
 func decodeConfigFile(configName string) {
     file := openConfigFile(configName)
     decoder := json.NewDecoder(file)
     err := decoder.Decode(&config)
     for err != nil {
         fmt.Println("Error: cannot decode the config file, please make sure it's a correct cofig file.")
         configName = getConfigName()
         file = openConfigFile(configName)
         decoder = json.NewDecoder(file)
         err = decoder.Decode(&config)
     }
 }

 /*
  * print out all nodes' name
  */
func printNodesName(nodes []Node) {
    fmt.Println("Possiable node names are: ")
	for _, node := range nodes {
        fmt.Printf("\t%s\n", node.Name)
	}
}

 /*
  * find the localName from config file
  * @param localName the name of local node
  */
  func findNodeFromConf(localName string) {
      var err error
      localNode, err = FindNodeByName(config.Nodes, localName)
      for err != nil {
          fmt.Println("Error: cannot find the local node's name in config file, please set the local name again.")
          printNodesName(config.Nodes)
          localName = getLocalName()
          localNode, err = FindNodeByName(config.Nodes, localName)
      }
  }

/*
 * initialize MessagePasser, this is a public method
 **/
func InitMessagePasser(configName string, localName string) {
    decodeConfigFile(configName)
    findNodeFromConf(localName)

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
