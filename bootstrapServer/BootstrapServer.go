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
 * send TCP messages
 * @param   conn – connection to send message over
 * @param   message – message to be sent
 **/
func sendMessageTCP(nodeName string, message *Message) {
    encoder := gob.NewEncoder(connections[nodeName])
    encoder.Encode(message)
}

/*
 * receive TCP messages
 * @param   conn – the connection to use
 *
 * @return  message
 **/
func receiveMessageTCP(conn net.Conn) (Message, error) {
    dec := gob.NewDecoder(conn)
    msg := &Message{}
    err := dec.Decode(msg)
    if err != nil {
        return *msg, err
    }
    return *msg, nil
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


//Main function, listens on TCP socket and tells a client hello
func main() {
    l, err := net.Listen("tcp", listenAddr)
    if err != nil {
        log.Fatal(err)
    }
    for {
        c, err := l.Accept()
        //Catch Errors
        if err != nil {
            log.Fatal(err)
        }
        //Tell the connected client Hello
        //TODO: This is a placeholder, remove it
        fmt.Fprintln(c, "Hello!")
        c.Close()
    }
}

/* the Main function of the Multegula application */
func main() {