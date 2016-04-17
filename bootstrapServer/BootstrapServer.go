////////////////////////////////////////////////////////////
//Multegula - BootstrapServer.go
//Bootstrapping/Grouping Server for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package main

import (
	"encoding/gob"
	"flag"
	"fmt"
	"net"
	"strconv"
	"strings"
	"time"
	"github.com/arminm/multegula/messagePasser"
)

type ClientInfo struct {
	Conn *net.Conn
	Node *messagePasser.Node
}

// constants
const MIN_PLAYERS_PER_GAME int = 2
const MAX_PLAYERS_PER_GAME int = 4
const TIMEOUT_DURATION = 30 * time.Second
const CHANNEL_SIZE = 10

//Declare a map of connections to nodes
var connections = make(map[net.Addr]*net.Conn)
var nodes = make(map[net.Addr]*messagePasser.Node)
var addClientChannel = make(chan ClientInfo, CHANNEL_SIZE)
var removeClientChannel = make(chan ClientInfo, CHANNEL_SIZE)
var timeoutTimer *time.Timer = time.NewTimer(time.Second)

/*
 * Handle Connections
 *
 * @param connection
 *        the connection object
 *
 **/
func handleConnection(conn net.Conn) {
	// keep track of having already added a connection to keep the loop running
	// in case the client got disconnected, so we can remove the added connection
	// from our maps. If the disconnect happens before we add the conn to our maps
	// then we just simply return from the function.
	haveAddedConnection := false
	for {
		nodePtr, err := receiveNode(conn)
		if err != nil {
			if err.Error() == "EOF" {
				fmt.Println("Got disconnected from", conn.RemoteAddr())
			} else {
				fmt.Println("Disconnecting:", conn.RemoteAddr())
			}
			if haveAddedConnection {
				removeClientChannel <- ClientInfo{&conn, nil}
			}
			return
		} else if (*nodePtr == messagePasser.Node{}) {
			fmt.Println("Received empty Node.")
			conn.Close()
			return
		}
		if haveAddedConnection == false {
			// we have to set the public ip of the client, since the client itself
			// doesn't know what their public ip is.
			ip := strings.Split(conn.RemoteAddr().String(), ":")[0]
			(*nodePtr).IP = ip
			addClientChannel <- ClientInfo{&conn, nodePtr}
			haveAddedConnection = true
		}
	}
}

/* Main function.
* Listens on provided port or default (55555)
**/
func main() {

	//Set port from command line
	portFlag := flag.Int("port", 55555, "Port to listen on for connections.")
	flag.Parse()
	fmt.Println("Multegula Bootstrap Server listening on TCP Port: ", *portFlag)

	//And listen
	ln, err := net.Listen("tcp", ":"+strconv.Itoa(*portFlag))
	if err != nil {
		fmt.Println("Couldn't start Bootstrap Server!")
		panic(err)
	}

	// Start the routine that manages connections and calls startAGame()
	go receiveConnections()

	//Loop forever
	for {
		//Begin accepting connections
		conn, err := ln.Accept()
		if err != nil {
			fmt.Println(err)
			continue
		}
		//Spawn thread to handle connections
		fmt.Println("Connection received from:", conn.RemoteAddr())
		go handleConnection(conn)
	}
}

/*
 * The routine to manage connections and trigger startAGame
 */
func receiveConnections() {
	// Make sure the timer is not running.
	timeoutTimer.Stop()

	for {
		//wait for new connections or disconnections, or for a timeout if there's one
		select {
		case clientInfo := <-addClientChannel:
			// check for duplicates
			if !duplicateNameExists(nodes, clientInfo.Node.Name) {
				connAddr := (*clientInfo.Conn).RemoteAddr()
				connections[connAddr] = clientInfo.Conn
				nodes[connAddr] = clientInfo.Node

				fmt.Printf("We have %v connections now!\n", len(connections))
				fmt.Printf("New Client: %+v\n", clientInfo.Node)
			} else {
				fmt.Println("Closing connection! Duplicate Node Name: ", clientInfo.Node.Name)
				(*clientInfo.Conn).Close()
			}
		case clientInfo := <-removeClientChannel:
			connAddr := (*clientInfo.Conn).RemoteAddr()
			if node, ok := nodes[connAddr]; ok {
				fmt.Printf("Removing Client: %+v\n", node)
				delete(connections, connAddr)
				delete(nodes, connAddr)
				fmt.Printf("We have %v connections now!\n", len(connections))
			}
		case <-timeoutTimer.C:
			//This is the case that handles our timeouts if we don't get enough players
			if len(connections) >= MIN_PLAYERS_PER_GAME {
				fmt.Printf("Timed out, starting with %v players!\n", len(connections))
				startAGame()
			}
		}

		if len(connections) == MIN_PLAYERS_PER_GAME {
			//Reset our timeoutTimer
			fmt.Println("Two connections established, starting countdown to game.")
			timeoutTimer.Reset(TIMEOUT_DURATION)
		} else if len(connections) == MAX_PLAYERS_PER_GAME {
			// Stop the timeoutTimer
			timeoutTimer.Stop()
			startAGame()
		}
	}
}

/*
 * check for duplicate names in a map of nodes
 */
func duplicateNameExists(existingNodes map[net.Addr]*messagePasser.Node, newNodeName string) bool {
	for _, node := range existingNodes {
		if node.Name == newNodeName {
			return true
		}
	}
	return false
}

/*
 * The synchronous function to start a game with 2-4 players and clear
 * the connections map for next games.
 */
func startAGame() {
	//Give everyone their player list
	for connAddr, connection := range connections {
		fmt.Println("Sending Peers to:", nodes[connAddr].Name)
		sendNodes(nodesForClient(connAddr), *connection)
		(*connection).Close()
	}

	//Clear the maps
	for connAddr := range connections {
		delete(connections, connAddr)
		delete(nodes, connAddr)
	}
}

// returns the list of peer nodes excluding the client
func nodesForClient(clientAddr net.Addr) *[]messagePasser.Node {
	peerNodes := []messagePasser.Node{}
	for connAddr := range connections {
		if connAddr != clientAddr {
			peerNodes = append(peerNodes, *nodes[connAddr])
		}
	}
	return &peerNodes
}

/*
 * sends nodes by encoding the array of nodes
 */
func sendNodes(nodes *[]messagePasser.Node, conn net.Conn) {
	encoder := gob.NewEncoder(conn)
	encoder.Encode(*nodes)
}

/*
 * received a single node struct
 */
func receiveNode(conn net.Conn) (*messagePasser.Node, error) {
	dec := gob.NewDecoder(conn)
	node := &messagePasser.Node{}
	err := dec.Decode(node)
	if err != nil {
		return node, err
	}
	return node, nil
}
