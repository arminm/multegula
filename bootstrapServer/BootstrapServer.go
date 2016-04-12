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
    clientChannel := make(chan Client)
    connectionChannel := make(chan net.Conn)

    //Spawn thread to handle messages
    go handleClients(clientChannel, connectionChannel)

    //Infinitely accept connections from clients
    for {
        conn, err := ln.Accept()
        if err != nil {
            fmt.Println(err)
            continue
        }
        //Spawn thread to handle connections
        go handleConnection(conn, clientChannel, connectionChannel)
    }
}

func handleConnection(conn net.Conn, clientChannel chan<- Client, connectionChannel chan<- net.Conn) {
    ch := make(chan string)
    clientChannel <- Client{conn, ch}

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

    //Wait until we get four players and then GO GO GO
    for len(connectionChannel) < MAX_PLAYERS_PER_GAME {}

    //Send our player list out to all connected clients
    conn.Write([]byte("PLAYER_LIST_BEGIN\n"))
    conn.Close()

    fmt.Printf("Connection from client %v closed.\n", conn.RemoteAddr())
    connectionChannel <- conn
}

func handleClients(clientChannel <-chan Client, connectionChannel <-chan net.Conn) {
    
    //Make a map of all clients
    clients := make(map[net.Conn]chan<- string)

    for {
        select {
        case client := <-clientChannel:
            fmt.Printf("New client connected: %v\n", client.conn)
            clients[client.conn] = client.ch
        case conn := <-connectionChannel:
            fmt.Printf("Client has disconnected: %v\n", conn)
            delete(clients, conn)
        }
    }
}