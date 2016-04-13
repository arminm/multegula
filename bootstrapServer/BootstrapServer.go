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
)

// constants
const MAX_PLAYERS_PER_GAME int = 4

//Declare a map of connections to nodes
var connections = make(map[net.Addr]net.Conn)

/*
 * Handle Connections
 *
 * @param connection
 *        the connection object
 *
 * @param addChannel
 *        A channel used for adding clients
 *
 * @param removeChannel
 *        A channel used for removing connections
 *
 **/
func handleConnection(conn net.Conn) {
	defer conn.Close()

	bufc := bufio.NewReader(conn)

	//Introduce ourselves to the client with these strings
	conn.Write([]byte("MULTEGULA_BOOTSTRAP_SERVER\n"))
	conn.Write([]byte("CLIENT_INTRODUCE_YOURSELF_NOW\n"))

	for {
		//Then the client should respond with its introduction message.
		raw, _, err := bufc.ReadLine()
		if err != nil {
			if err.Error() == "EOF" {
				fmt.Println("Got disconnected from", conn.RemoteAddr())
				delete(connections, conn.RemoteAddr())
				fmt.Printf("We have %v connections now!\n", len(connections))
				break
			} else {
				fmt.Println("Not disconnecting but got error:", err.Error())
				continue
			}
		}

		//Accept the client's message
		message := string(raw)
		fmt.Printf("%v:%v\n", conn.RemoteAddr(), message)
		//Tell the client that we've acknowledged their connection.
		//Client will now wait to receive their group message.
		conn.Write([]byte("WELCOME_CLIENT_" + message + "\n"))
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

	//And connect
	ln, err := net.Listen("tcp", ":"+strconv.Itoa(*portFlag))
	if err != nil {
		fmt.Println("Couldn't start Bootstrap Server!")
		panic(err)
	}

	for {
		//Wait until we get four players and then GO GO GO
		conn, err := ln.Accept()
		if err != nil {
			fmt.Println(err)
			continue
		}
		//Spawn thread to handle connections
		fmt.Println("Connection received from:", conn.RemoteAddr())
		go handleConnection(conn)

		// Keep track of connections. Once we have 4 connections, we can spin off a game...
		connections[conn.RemoteAddr()] = conn
		fmt.Printf("We have %v connections now!\n", len(connections))

	}
}
