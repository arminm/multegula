////////////////////////////////////////////////////////////
//Multegula - BootstrapServer.go
//Bootstrapping/Grouping Server for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package main

import (
	"bufio"
	"flag"
	"fmt"
	"net"
	"strconv"
	"time"
)

// constants
const MIN_PLAYERS_PER_GAME int = 2
const MAX_PLAYERS_PER_GAME int = 4
const timeOutDuration = 30 * time.Second

//Declare a map of connections to nodes
var connections = make(map[net.Addr]net.Conn)
var addConnectionChannel = make(chan net.Conn, 10)
var removeConnectionChannel = make(chan net.Conn, 10)
var timeoutTimer *time.Timer = time.NewTimer(time.Second)

/*
 * Handle Connections
 *
 * @param connection
 *        the connection object
 *
 **/
func handleConnection(conn net.Conn) {
	bufc := bufio.NewReader(conn)

	//Introduce ourselves to the client with these strings
	conn.Write([]byte("MULTEGULA_BOOTSTRAP_SERVER\n"))
	conn.Write([]byte("CLIENT_SAY_HELLO_NOW\n"))

	for {
		//Then the client should respond with its introduction message.
		raw, _, err := bufc.ReadLine()
		if err != nil {
			if err.Error() == "EOF" {
				fmt.Println("Got disconnected from", conn.RemoteAddr())
				// Set conn to be removed
				removeConnectionChannel <- conn
				break
			} else {
				fmt.Println("Not disconnecting but got error:", err.Error())
				continue
			}
		}

		//Accept the client's message, add them to
		message := string(raw)
		fmt.Printf("Got message from: %v:%v\n", conn.RemoteAddr(), message)

		//Check to ensure it was valid.
		//The \n seems to mess this up little bit when using nc, maybe we can put it back in for network comms.
		if message == "MULTEGULA_CLIENT_HELLO" {
			//Tell the client that we've acknowledged their connection.
			//Client will now wait to receive their group message.
			conn.Write([]byte("WELCOME_CLIENT\n"))
			// set conn to be added
			addConnectionChannel <- conn

			return
		} else {
			conn.Write([]byte("ERR_INCORRECT_IDENTIFICATION\n"))
			fmt.Printf("Didn't receive correct hello. Disconnecting client.\n")
			conn.Close()
			return
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
		case connection := <-addConnectionChannel:
			connections[connection.RemoteAddr()] = connection
			fmt.Printf("We have %v connections now!\n", len(connections))
		case connection := <-removeConnectionChannel:
			delete(connections, connection.RemoteAddr())
			fmt.Printf("We have %v connections now!\n", len(connections))
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
			timeoutTimer.Reset(timeOutDuration)
		} else if len(connections) == MAX_PLAYERS_PER_GAME {
			// Stop the timeoutTimer
			timeoutTimer.Stop()
			startAGame()
		}
	}
}

/*
 * The synchronous function to start a game with 2-4 players and clear
 * the connections map for next games.
 */
func startAGame() {
	//Give everyone their player list
	for connection := range connections {
		connections[connection].Write([]byte("PLAYER_LIST_BEGIN\n"))
		for peerConnection := range connections {
			connections[connection].Write([]byte(peerConnection.String() + "\n"))
		}
		connections[connection].Write([]byte("PLAYER_LIST_END\n"))
		connections[connection].Close()
	}

	//Clear the map
	for connection := range connections {
		delete(connections, connection)
	}
}
