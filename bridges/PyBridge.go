////////////////////////////////////////////////////////////
//Multegula - PyBridge.go
//Server for interacting with UI written in Python
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package bridges

import (
	"bufio"
	"fmt"
	"net"
	"reflect"
	"strconv"
	"strings"

	"github.com/arminm/multegula/messagePasser"
)

// TODO: Remove fixed port number
/* port number for local TCP connection */
// const port string = ":44444"

/* delimiter for formating message */
const delimiter string = "##"

/* the queue for messages to be sent to multegula */
var sendQueue chan messagePasser.Message = make(chan messagePasser.Message, messagePasser.QUEUE_SIZE)

/* the queue for messages received from multegula */
var receivedQueue chan messagePasser.Message = make(chan messagePasser.Message, messagePasser.QUEUE_SIZE)

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

/*
 * go routine for putting message to sendQueue
 * @param message - message to be put into sendQueue
 */
func putMessageToSendQueue(message messagePasser.Message) {
	sendQueue <- message
}

/*
 * go routine for putting message to receivedQueue
 * @param message - message to be put into receivedQueue
 */
func putMessageToReceivedQueue(message messagePasser.Message) {
	receivedQueue <- message
}

/*
 * receive a message from PyBridge, this method will be called by multegula
 * if there is no message in the sendQueue, it will block
 * @return the message received from PyBridge
 */
func ReceiveFromPyBridge() messagePasser.Message {
	message := <-sendQueue
	return message
}

/*
 * send a message to PyBridge, this method will be called by multegula
 * @param message
 *        the message to be sent to PyBridge
 */
func SendToPyBridge(message messagePasser.Message) {
	go putMessageToReceivedQueue(message)
}

/**
 * receive messages from UI and send to message passer
 * @param conn
 *        local connection for interacting with UI
 **/
func receiveFromUI(conn net.Conn) {
	for {
		messageString, _ := bufio.NewReader(conn).ReadString('\n')
		if len(messageString) > 0 {
			fmt.Printf("PyBridge: Message received from UI: %s\n", messageString[0:len(messageString)-1])
			go putMessageToSendQueue(decodeMessage(messageString[0 : len(messageString)-1]))
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
		var message messagePasser.Message = <-receivedQueue
		if (!reflect.DeepEqual(message, messagePasser.Message{})) {
			fmt.Printf("PyBridge: Message sent to UI: %s\n", encodeMessage(message))
			conn.Write([]byte(encodeMessage(message) + "\n"))
		}
	}
}

func InitPyBridge(port int) {
	portStr := ":" + strconv.Itoa(port)
	ln, err := net.Listen("tcp", portStr)
	if err != nil {
		fmt.Println(err)
	}

	conn, _ := ln.Accept()

	/* start a new routine to receive messages from UI */
	go receiveFromUI(conn)

	/* start a new routine to send message to UI */
	go sendToUI(conn)
}
