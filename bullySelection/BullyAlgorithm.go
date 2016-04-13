////////////////////////////////////////////////////////////
//Multegula - BullyAlgorithm.go
//Multicasting Message Passer for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////
//This file implements the bull algorithm which will be used
//for selecting unicorn in multegula. The unicorn will send
//heart beats to others nodes to tell others he is alive.
////////////////////////////////////////////////////////////

package bullySelection

import (
	"github.com/arminm/multegula/messagePasser"
)

/* If a node doesn't receive message from coordinator after 
 * after this time period, it will consider the coordinator
 * is lost or crashed. This time period includes the round-trip
 * transmission delay and message processing delay. It is counted
 * in millisecond.
 */
const LIVENESS_TIMEOUT int = 200

/* This is the time a node will wait after sending out an answer
 * message. If it receives coordinator message within this time
 * period, it will know which node is the new unicorn; otherwise,
 * it will start another election.
 */
const WAITING_COORDINATOR_MESSAGE int = 100

/* The kinds of message will be used in bully algorithm */
/* The election message */
const ELECTION string = "election"
/* The answer message */
const ANSWER string = "answer"
/* The coordinator message */
const COORDINATOR string = "coordinator"

/* The name of node */
var localName string

/* Nodes whose names are smaller than local name in the group */
var frontNodes []string

/* Nodes whose names are greater than local name in the group */
var latterNodes []string

/* 
 * The size of queue: sendQueue, receivedQueue
 */
const QUEUE_SIZE int = 100

/* This is the message kind unicorn will send to other nodes
 * to let other nodes know that it is alive
 */
const MSG_ALIVE string = "MSG_ALIVE"

/* The queue for messages to be sent, messages in this queue
 * will be passed to messagePasser by mutegula
 */
var sendChannel chan messagePasser.Message = make(chan messagePasser.Message, 100)

/*
 * Put message into sendChannel
 * @param	message - message to be put into sendChannel
 */
func putMessageToSendChannel(message messagePasser.Message) {
	sendChannel <- message
}

/*
 * Get message from sendChannel. This method will be called
 * in mutegula and it's a public message
 * @return	the message got from sendChannel
 */
func GetMessageFromSendChannel() messagePasser.Message {
	message := <- sendChannel
}

/* The queue for received messages, mutegula will put messages,
 * which come from messagePasser, into this queue
 */
var receiveChannel chan messagePasser.Message = make(chan messagePasser.Message, 100)

/*
 * Put message into receiveChannel. This method will be called
 * in mutegula and it's a public message
 * @param	message - message to be put into receiveChannel
 */
func PutMessageToReceiveChannel(message messagePasser.Message) {
	receiveChannel <- message
}

/*
 * Get message from receiveChannel
 * @return	the message got from receiveChannel
 */
func getMessageFromReceiveChannel() messagePasser.Message {
	message := <- receiveChannel
}

/*
 * Separate nodes' name into two parts based on lexicographical order
 * @param	nodes
 *			the names of all nodes in the group
 *
 * @param	localNode
 *			the name of this node
 *	
 * @return	frontNodes – nodes smaller than localName
 *			latterNodes – nodes greater thanlocalName
 **/
func getFrontAndLatterNodes(nodes []string, localName string) ([]string, []string) {
	frontNodes := []string{}
	latterNodes := []string{}
	for _, node := range nodes {
		if node < localName {
			frontNodes = append(frontNodes, node)
		} else if node > localName {
			latterNodes = append(latterNodes, node)
		}
	}
	return frontNodes, latterNodes
}

/* Unicorn send MSG_ALIVE message to other nodes */
func sendHeartBeat() {
	for _, name := range frontNodes {
		go putMessageToSendChannel(messagePasser.Message{
			Source: localName, 
			Destination: name, 
			Content: MSG_ALIVE, 
			Kind: MSG_ALIVE
			})
	}
}

/* Unicorn send COORDINATOR message to other nodes including it self */
func sendCoordinator() {
	for _, name := range frontNodes {
		go putMessageToSendChannel(messagePasser.Message{
			Source: localName,
			Destination: name,
			Content: COORDINATOR,
			Kind: COORDINATOR
			})
	}
	go putMessageToSendChannel(messagePasser.Message{
		Source: localName,
		Destination: localName,
		Content: COORDINATOR,
		Kind: COORDINATOR
		})
}

/* Node sends election message */
func sendElection() {
	for _, name := range latterNodes {
		go putMessageToSendChannel(messagePasser.Message{
			Source: localName,
			Destination: name,
			Content: ELECTION,
			Kind: ELECTION
			})
	}
}

/* Node reply answer message
 * @param	destination
 *			the destination of reply
 */
func sendAnswer(destination string) {
	go putMessageToSendChannel(messagePasser.Message{
		Source: localName,
		Destination: destination,
		Content:ANSWER,
		Kind: ANSWER
		})
}

/*
 * Initialize the bully algorithm, and start the first selection
 * @param	name
 *			the name of this node
 *
 * @param	names
 *			the names of all nodes in the group
 */
func InitBullySelection(name string, names []string) {
	localName = name
	frontNodes, latterNodes = getFrontAndLatterNodes(names, localName)
}
