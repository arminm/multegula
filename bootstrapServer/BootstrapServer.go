////////////////////////////////////////////////////////////
//Multegula - BootstrapServer.go
//Bootstrapping/Grouping Server for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package main

import (
    "fmt"
    "log"
    "net"
    "strings"
    "sync"
    "encoding/gob"
    "encoding/json"
    "errors"
    "sort"
    "strconv"
)

// constants
const MULTEGULA_DNS string = "multegula.dyndns.org"
const MAX_PLAYERS_PER_GAME int = 4
const MULTICAST_DEST string = "EVERYBODY"
const DEFAULT_LISTEN_PORT = "localhost:55555"

// Node structure to hold each node's information
type Node struct {
    Name string
    IP   string
    Port int
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
    Timestamp   []int
}

// required functions to implement the sort.Interface for sorting Nodes
type Nodes []Node

func (slice Nodes) Len() int {
    return len(slice)
}

func (slice Nodes) Less(i, j int) bool {
    return slice[i].Name < slice[j].Name
}

func (slice Nodes) Swap(i, j int) {
    slice[i], slice[j] = slice[j], slice[i]
}

//Wait for enough connections before continuing
var wg sync.WaitGroup

/* map stores connections to each node
 * <key, value> = <name, connection>
 **/
var connections map[string]net.Conn = make(map[string]net.Conn)

func getConnectionName(connection net.Conn) (string, error) {
    for name, conn := range connections {
        if conn == connection {
            return name, nil
        }
    }
    return "Not Found", fmt.Errorf("Connection not found:%v\n", connection)
}

/*
 * finds a node within an array of nodes by Name
 */
func findNodeByName(nodes []Node, name string) (int, Node, error) {
    for i, node := range nodes {
        if node.Name == name {
            return i, node, nil
        }
    }
    return -1, Node{}, errors.New("Node not found: " + name)
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
 * accepts connections from other nodes and stores
 * connections into connections map, after accepting
 * all connections from all other nodes in the group,
 * this routine exits
 * @param   frontNodes
 *          map that contains all nodes with smaller Node names
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
        msg, _ := receiveMessageTCP(conn)
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
 * construct message from it's string format
 * @param   messageString
 *          message in string format
 *
 * @return  message
 **/
func decodeMessage(messageString string) Message {
    var elements []string = strings.Split(messageString, delimiter)
    return messagePasser.Message{Source: elements[0], Destination: elements[1], Content: elements[2], Kind: elements[3]}
}

/*
 * convert message to string
 * @param   message
 *          message to be converted
 *
 * @return  the string format of the message
 **/
func encodeMessage(message Message) string {
    return message.Source + delimiter + message.Destination + delimiter + message.Content + delimiter + message.Kind
}

/*
 * Tells nodes to start the game
 **/
func acceptConnection(frontNodes map[string]Node, localNode Node) {
    //TODO
}


//Main function, listens on TCP socket and tells a client hello
func main() {
    portStr := ":" + strconv.Itoa(port)
    ln, err := net.Listen("tcp", portStr)
    if err != nil {
        fmt.Println(err)
    }

    conn, _ := ln.Accept()

    /* start a new routine to receive messages from UI */
    go receiveFromUI(conn)

    /* start a new routine to send message to UI */
    go sendToUI(conn)
}