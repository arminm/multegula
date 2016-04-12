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
const MULTEGULA_DNS string = "multegula.dyndns.org"
const MAX_PLAYERS_PER_GAME int = 4
const MULTICAST_DEST string = "EVERYBODY"
const DELIMITER string = "##"

type Client struct {
    conn net.Conn
    ch   chan<- string
}


/* Main function.  
* Listens on provided port or default (55555), 
* spawns a thread to accept connections and add them to a map,
* then sends a message to each node in the group indicating that the
* game has started.
**/
func main() {
    //Set port from command line
    portFlag := flag.Int("port", 55555, "Port to listen on for connections.")
    flag.Parse()
    fmt.Println("Multegula Bootstrap Server listening on: ", *portFlag)
    
    //And connect
    ln, err := net.Listen("tcp", ":"+strconv.Itoa(*portFlag))
    if err != nil {
        fmt.Println("Couldn't start Bootstrap Server!")
        panic(err)
        os.Exit(1)
    }

    //Make channels to handle messages, clients, and connections
    msgchan := make(chan string)
    addchan := make(chan Client)
    rmchan := make(chan net.Conn)

    //Spawn thread to handle messages
    go handleMessages(msgchan, addchan, rmchan)

    //Infinitely accept connections from clients
    for {
        conn, err := ln.Accept()
        if err != nil {
            fmt.Println(err)
            continue
        }
        //Spawn thread to handle connections
        go handleConnection(conn, msgchan, addchan, rmchan)
    }
}

func handleConnection(c net.Conn, msgchan chan<- string, addchan chan<- Client, rmchan chan<- net.Conn) {
    ch := make(chan string)
    msgs := make(chan string)
    addchan <- Client{c, ch}

    //Spawns a function that handles connections for new clients.
    go func() {
        defer close(msgs)
        bufc := bufio.NewReader(c)

        //Introduce ourselves to the client with these strings
        c.Write([]byte("MULTEGULA_BOOTSTRAP_SERVER\n"))
        c.Write([]byte("CLIENT_INTRODUCE_YOURSELF_NOW\n"))

        //Then the client should respond with its introduction message.
        nick, _, err := bufc.ReadLine()
        if err != nil {
            fmt.Println("Something went wrong when the client was introducing itself.")
            return
        }

        //Accept the client's nickname
        nickname := string(nick)

        //Tell the client that we've acknowledged their connection
        c.Write([]byte("WELCOME_CLIENT_" + nickname + "\n"))

        //Not sure if the client will be communicating any more or not.
        //This is for that - REMOVE for actual operation.
        for {
            line, _, err := bufc.ReadLine()
            if err != nil {
                break
            }
            msgs <- nickname + ": " + string(line)
        }
    }()

LOOP:
    for {
        select {
        case msg, ok := <-msgs:
            if !ok {
                break LOOP
            }
            msgchan <- msg
        case msg := <-ch:
            _, err := c.Write([]byte(msg))
            if err != nil {
                break LOOP
            }
        }
    }

    c.Close()
    fmt.Printf("Connection from client %v closed.\n", c.RemoteAddr())
    rmchan <- c
}

func handleMessages(msgchan <-chan string, addchan <-chan Client, rmchan <-chan net.Conn) {
    
    //Make a map of all clients
    clients := make(map[net.Conn]chan<- string)

    for {
        select {
        case msg := <-msgchan:
            fmt.Printf("Received a message from client: %s\n", msg)
            for _, ch := range clients {
                go func(mch chan<- string) { 
                    mch <- "\033[1;33;40m" + msg + "\033[m\r\n" }(ch)
                }
        case client := <-addchan:
            fmt.Printf("New client observed: %v\n", client.conn)
            clients[client.conn] = client.ch
        case conn := <-rmchan:
            fmt.Printf("Client has disconnected: %v\n", conn)
            delete(clients, conn)
        }
    }
}