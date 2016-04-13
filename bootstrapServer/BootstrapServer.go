////////////////////////////////////////////////////////////
//Multegula - BootstrapServer.go
//Bootstrapping/Grouping Server for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package main

import (
    "flag"
    "fmt"
    "net"
    "strconv"
    "os"
    "bufio"
)

// constants
const MAX_PLAYERS_PER_GAME int = 4

type Client struct {
    conn net.Conn
    ch   chan<- string
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
        os.Exit(1)
    }

    //Make channels to handle clients and connections
    addChannel := make(chan Client)
    removeChannel := make(chan net.Conn)
    //Make a map of all clients
    clients := make(map[net.Conn]chan<- string)

    //Spawn thread to handle messages
    go handleClients(addChannel, removeChannel)

    //Wait until we get four players and then GO GO GO
    for len(addChannel) < MAX_PLAYERS_PER_GAME {
        conn, err := ln.Accept()
        if err != nil {
            fmt.Println(err)
            continue
        }
        //Spawn thread to handle connections
        go handleConnection(conn, addChannel, removeChannel)

        fmt.Println("Clients Connected: ",len(clients))
    }
    //Once we have four, send out our player list to all connected clients
    //conn.Write([]byte("PLAYER_LIST_BEGIN\n"))

}

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
func handleConnection(conn net.Conn, addChannel chan<- Client, removeChannel chan<- net.Conn) {
    ch := make(chan string)
    addChannel <- Client{conn, ch}

    bufc := bufio.NewReader(conn)

    //Introduce ourselves to the client with these strings
    conn.Write([]byte("MULTEGULA_BOOTSTRAP_SERVER\n"))
    conn.Write([]byte("CLIENT_INTRODUCE_YOURSELF_NOW\n"))

    //Then the client should respond with its introduction message.
    nick, _, err := bufc.ReadLine()
    if err != nil {
        fmt.Println("Something went wrong when the client was introducing itself.")
        return
    }

    //Accept the client's nickname
    nickname := string(nick)

    //Tell the client that we've acknowledged their connection.
    //Client will now wait to receive their group message.
    conn.Write([]byte("WELCOME_CLIENT_" + nickname + "\n"))

    //Wait forever.
    for {}

    //Clean up this connection.
    conn.Close()
    fmt.Printf("Connection from client %v closed.\n", conn.RemoteAddr())
    removeChannel <- conn
}

/*
 * Handle Clients
 *
 * @param addChannel
 *        A channel used for adding clients
 *
 * @param removeChannel
 *        A channel used for removing connections
 *
 *
 **/
func handleClients(addChannel <-chan Client, removeChannel <-chan net.Conn) {
    
    //Make a map of all clients
    clients := make(map[net.Conn]chan<- string)

    for {
        select {
        case client := <-addChannel:
            fmt.Printf("New client connected: %v\n", client.conn)
            clients[client.conn] = client.ch
        case conn := <-removeChannel:
            fmt.Printf("Client has disconnected: %v\n", conn)
            delete(clients, conn)
        }
    }
}