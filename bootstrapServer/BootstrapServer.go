////////////////////////////////////////////////////////////
//Multegula - BootstrapServer.go
//Bootstrapping/Grouping Server for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package main

import (
    "flag"
    "fmt"
    "log"
    "net"
    "strings"
    "sync"
    "encoding/gob"
    "encoding/json"
    "errors"
    "strconv"
    "time"
)

// constants
const MULTEGULA_DNS string = "multegula.dyndns.org"
const MAX_PLAYERS_PER_GAME int = 4
const MULTICAST_DEST string = "EVERYBODY"
const DELIMITER string = "##"

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

/* map stores connections to each node
 * <key, value> = <name, connection>
 **/
var connections map[string]net.Conn = make(map[string]net.Conn)

/*
 * accepts connections from other nodes and stores
 * connections into connections map
 **/
func acceptConnections() {
    for {
        fmt.Println("Multegula Bootstrap Server listening on: ", strconv.Itoa(portFlag))
        ln, err := net.Listen("tcp", ":"+strconv.Itoa(portFlag))
        if err != nil {
            fmt.Println("Couldn't start Bootstrap Server!")
            panic(err)
        }
        //Accept connection
        conn, _ := ln.Accept()

        //Get remote address of connection
        fmt.Println("Connection received from: ", conn.RemoteAddr())

        //Client will send a message introducing itself as soon as it's connected
        msg, _ := receiveMessageTCP(conn)
        fmt.Println("Client introduced itself as ", msg.Source, " at ", conn.RemoteAddr())

        connections[msg.Source] = conn
    }
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
 * send TCP messages
 * @param   conn – connection to send message over
 * @param   message – message to be sent
 **/
func sendMessageTCP(nodeName string, message *Message) {
    encoder := gob.NewEncoder(connections[nodeName])
    encoder.Encode(message)
}

/*
 * construct message from its string format
 * @param   messageString
 *          message in string format
 *
 * @return  message
 **/
func decodeMessage(messageString string) Message {
    var elements []string = strings.Split(messageString, DELIMITER)
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
    return message.Source + DELIMITER + message.Destination + DELIMITER + message.Content + DELIMITER + message.Kind
}


/* Main function.  
* Listens on provided port or default (55555), 
* spawns a thread to accept connections and add them to a map,
* then sends a message to each node in the group indicating that the
* game has started.
**/
func main() {
        portFlag := flag.Int("port", 55555, "Port to listen on for connections.")
        ln, err := net.Listen("tcp", portFlag)
        if err != nil {
            fmt.Println(err)
        }
        
        //Spawn thread to listen for connections
        go acceptConnections()
        
        //Wait for a group of four, then start
        //TODO: If 60 seconds passes and four nodes haven't joined, start game with two or three
        while len(connections) < 4 {
            //Do nothing, just wait
        }

        //Spin off clients into their own game.
        //Will need to send a message including everybody's name and IP/Port information
        groupMessage = "BOOTSTRAPSERVER"+ DELIMITER + "EVERYBODY" + DELIMITER + message.Content + DELIMITER + "MSG_GROUP"

        for connection := range connections {
            sendMessageTCP(connection, groupMessage)
        }

        //Clear connection map and wait for new 
        for key := range connections {
            delete(connections, key)
        }
    }

}