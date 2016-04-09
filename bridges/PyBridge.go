////////////////////////////////////////////////////////////
//Multegula - PyBridge.go 
//Server for interacting with UI written in Python
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package bridges

import (
    "fmt"
    "net"
    "bufio"
    "github.com/arminm/multegula/messagePasser"
    "strings"
)

/* port number for local TCP connection */
const port string = ":44444"

/* delimiter for formating message */
const delimiter string = "##"

/*
 * construct message from it's string format
 * @param	messageString
 *			message in string format
 *
 * @return	message
 **/
func decodeMessage(messageString string) messagePasser.Message {
	var elements []string = strings.Split(messageString, delimiter)
	return messagePasser.Message{Source: elements[0], Destination: elements[1], Content: elements[2], Kind: elements[3]}
}

/* 
 * convert message to string
 * @param	message
 *			message to be converted
 *
 * @return	the string format of the message
 **/
func encodeMessage(message messagePasser.Message) string {
	return message.Source + delimiter + message.Destination + delimiter + message.Content + delimiter + message.Kind
}

/**
 * receive messages from UI and send to message passer
 * @param conn
 *        local connection for interacting with UI
 **/
func receiveFromUI(conn net.Conn) {
    for {
        messageString, _ := bufio.NewReader(conn).ReadString('\n')
        if(len(messageString) > 0) {
            fmt.Printf("PyBridge: Message received from UI: %s\n", messageString[0:len(messageString) - 1])
            messagePasser.Send(decodeMessage(messageString[0:len(messageString) - 1]))
        }
    }
}

/**
 * receive messages from message passer and send to UI
 * @param conn
 *        local connection for interacting with UI
 **/
func sendToUI(conn net.Conn) {
    for {
        var message messagePasser.Message = messagePasser.BlockReceive()
        if(message != messagePasser.Message{}) {
            fmt.Printf("PyBridge: Message sent to UI: %s\n", encodeMessage(message))
            conn.Write([]byte(encodeMessage(message) + "\n"))
        }
    }
}

func InitPyBridge(configFile string, localName string) {
    messagePasser.InitMessagePasser(configFile, localName)

    ln, err := net.Listen("tcp", port)
    if(err != nil) {
        fmt.Println(err)
    }

    conn, _ := ln.Accept()

    /* start a new routine to receive messages from UI */
    go receiveFromUI(conn)

    sendToUI(conn)
}
