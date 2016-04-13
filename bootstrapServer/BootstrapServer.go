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
	conn.Write([]byte("CLIENT_SAY_HELLO_NOW\n"))

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
		fmt.Printf("Got hello from: %v:%v\n", conn.RemoteAddr(), message)
		//Tell the client that we've acknowledged their connection.
		//Client will now wait to receive their group message.
		conn.Write([]byte("WELCOME_CLIENT\n"))
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

    		//Keep track of connections. 
    		connections[conn.RemoteAddr()] = conn
    		fmt.Printf("We have %v connections now!\n", len(connections))

            //Only continue past here if we have at least 2 connections
            for len(connections) >= 2 {
            	//Set our timeout values
            	timeout := time.After(5 * time.Second)
				tick := time.Tick(500 * time.Millisecond)

	            fmt.Printf("At least two connections established, starting countdown to game.\n")
	            //Once we have 4 connections, we can spin off a game
	            //But timeout after 30 seconds if we have at least one connection...
	            TIMELOOP:
		            for{
						select {
							    case <- timeout:
							    	fmt.Printf("Timed out, starting with %v players!\n", len(connections))
							    	break TIMELOOP
							    case <- tick:
								    if len(connections) >= MAX_PLAYERS_PER_GAME{				    	
								    	break TIMELOOP
								    }
						}
					}
			    //Give everyone their player list
	            for connection := range connections {
	                connections[connection].Write([]byte("PLAYER_LIST_BEGIN\n"))
	                for peerConnection := range connections {
	                    connections[connection].Write([]byte(peerConnection.String()+"\n"))
	                }
	                connections[connection].Write([]byte("PLAYER_LIST_END\n"))
	            }
	            
	            //Clear the map
	            for connection := range connections {
	                delete(connections, connection)
	                //Closing the connection is having problems right now, not sure why.
	                //We can just have the clients do this as long as the map is clear.
	                //connections[connection].Close()
	            }
        	}
        }
    }
