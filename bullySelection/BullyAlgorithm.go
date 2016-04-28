////////////////////////////////////////////////////////////
//Multegula - BullyAlgorithm.go
//Multicasting Message Passer for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////
//This file implements the bull algorithm which will be used
//for selecting unicorn in multegula. Health check is used
//to check the health of selected unicorn
////////////////////////////////////////////////////////////

package bullySelection

import (
	"fmt"
	"strconv"
	"time"
	"strings"

	"github.com/arminm/multegula/defs"
	"github.com/arminm/multegula/messagePasser"
)

/* If a node doesn't receive message from unicorn after
 * after this time period, it will consider the unicorn
 * is lost or crashed. After sending out an election message,
 * the node waits TIMEOUT time for answer message.
 * This time period includes the round-trip
 * transmission delay and message processing delay. It is counted
 * in millisecond.
 */
const TIMEOUT int = 800

/* The time period between two health check */
const TIME_BETWEEN_HEALTH_CHECK = 1000

/* This is the time a node will wait after sending out an answer
 * message. If it receives unicorn message within this time
 * period, it will know which node is the new unicorn; otherwise,
 * it will start another election.
 */
const WAITING_UNICORN_MESSAGE_TIMEOUT int = 1200

/* The name of node */
var localName string

/* The name of unicorn */
var unicorn string

/* Nodes whose names are smaller than local name in the group */
var frontNodes []string

/* Nodes whose names are greater than local name in the group */
var latterNodes []string

/* The sequence number of message */
var seqNum int = -1

const SEQNUM_UPPER_BOUND int = 999999

/* The queue for messages to be sent, messages in this queue
 * will be passed to messagePasser by mutegula
 */
var sendChannel chan messagePasser.Message = make(chan messagePasser.Message, defs.QUEUE_SIZE)

/*
 * Put message into sendChannel
 * @param	message - message to be put into sendChannel
 */
func putMessageToSendChannel(message messagePasser.Message) {
	message.Content = message.Content + defs.DELIMITER + message.Destination
	message.Destination = defs.MULTICAST_DEST
	fmt.Printf("Message will be sent: %+v\n", message)
	sendChannel <- message
}

/*
 * Get message from sendChannel. This method will be called
 * in mutegula and it's a public message
 * @return	the message got from sendhannel
 */
func GetMessageFromSendChannel() messagePasser.Message {
	message := <-sendChannel
	return message
}

/*
 * When using reliable multicast, the destination of message is MULTICAST_DEST,
 * the realy destination of message is append after message.Content
 * @param	message 	message to be interpreted
 *
 * @return	the content and real destination of message 
 */
func getMessageContentAndDestination(message messagePasser.Message) (string, string) {
	elements := strings.Split(message.Content, defs.DELIMITER)
	return elements[0], elements[1]
}

/* The queue for received messages, mutegula will put messages,
 * which come from messagePasser, into this queue
 */
var receiveChannel chan messagePasser.Message = make(chan messagePasser.Message, defs.QUEUE_SIZE)

/*
 * Put message into receiveChannel. This method will be called
 * in mutegula and it's a public message
 * @param	message - message to be put into receiveChannel
 */
func PutMessageToReceiveChannel(message messagePasser.Message) {
	/* 
	 * If the muticast message's destination is this node,
	 * reconstruct this message; otherwise, the message is dropped
	 */
	 content, destination := getMessageContentAndDestination(message)
	if destination == localName {
		message.Content = content
		message.Destination = destination
		fmt.Printf("Message received: %+v\n", message)
		receiveChannel <- message
	}
}

/*
 * Get message from receiveChannel
 * @return	the message got from receiveChannel
 */
func getMessageFromReceiveChannel() messagePasser.Message {
	message := <-receiveChannel
	return message
}

/* received answer message */
var receivedAnswerChannel chan messagePasser.Message = make(chan messagePasser.Message, defs.QUEUE_SIZE)

/* received unicorn message */
var receivedUnicornChannel chan messagePasser.Message = make(chan messagePasser.Message, defs.QUEUE_SIZE)

/* received health check reply message */
var receivedHealthCheckReplyChannel chan messagePasser.Message = make(chan messagePasser.Message, defs.QUEUE_SIZE)

/*
 * this channel holds all unicorn update message,
 * whenever there are unicorn update, the unicorn
 * update message will be put into this channel so
 * that multegula can get the unicorn update
 */
var unicornUpdateChannel chan messagePasser.Message = make(chan messagePasser.Message, defs.QUEUE_SIZE)

func putUnicornUpdate(message messagePasser.Message) {
	unicornUpdateChannel <- message
}

func GetUnicornUpdate() messagePasser.Message {
	return <-unicornUpdateChannel
}

/* dispatch received message */
func dispatchMessage() {
	for {
		message := getMessageFromReceiveChannel()
		switch message.Kind {
		case defs.MSG_BULLY_ANSWER:
			go func() {
				receivedAnswerChannel <- message
			}()
		case defs.MSG_BULLY_UNICORN:
			go func() {
				receivedUnicornChannel <- message
			}()
		case defs.MSG_BULLY_ELECTION:
			sendAnswerMessage(message.Source, message.Content)
		case defs.MSG_BULLY_ARE_YOU_ALIVE:
			go putMessageToSendChannel(messagePasser.Message{
				Source:      localName,
				Destination: message.Source,
				Content:     message.Content,
				Kind:        defs.MSG_BULLY_IAM_ALIVE,
			})
		case defs.MSG_BULLY_IAM_ALIVE:
			go func() {
				receivedHealthCheckReplyChannel <- message
			}()
		}
	}
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
func getFrontAndLatterNodes(nodes messagePasser.Nodes, localName string) ([]string, []string) {
	frontNodes = []string{}
	latterNodes = []string{}
	for _, node := range nodes {
		if node.Name < localName {
			frontNodes = append(frontNodes, node.Name)
		} else if node.Name > localName {
			latterNodes = append(latterNodes, node.Name)
		}
	}
	return frontNodes, latterNodes
}

/* Unicorn send unicorn message to other nodes */
func sendUnicornMessage() {
	for _, name := range frontNodes {
		go putMessageToSendChannel(messagePasser.Message{
			Source:      localName,
			Destination: name,
			Content:     localName,
			Kind:        defs.MSG_BULLY_UNICORN,
		})
	}
}

/* Node sends election message
 * @param	timestamp
 *			the timestamp for this message
 */
func sendElectionMessage(timestamp string) {
	for _, name := range latterNodes {
		go putMessageToSendChannel(messagePasser.Message{
			Source:      localName,
			Destination: name,
			Content:     timestamp,
			Kind:        defs.MSG_BULLY_ELECTION,
		})
	}
}

/* Node reply answer message
 * @param	destination
 *			the destination of reply
 *
 * @param	timestamp
 *			the timestamp of received election message
 */
func sendAnswerMessage(destination string, timestamp string) {
	go putMessageToSendChannel(messagePasser.Message{
		Source:      localName,
		Destination: destination,
		Content:     timestamp,
		Kind:        defs.MSG_BULLY_ANSWER,
	})
}

/* Get the string representation of current time
 * @return	the current time in string format
 */
func getCurrentTime() string {
	seqNum = (seqNum + 1) % SEQNUM_UPPER_BOUND
	return strconv.Itoa(seqNum)
}

func sendHealthCheckRequestMessage(timestamp string) {
	go putMessageToSendChannel(messagePasser.Message{
		Source:      localName,
		Destination: unicorn,
		Content:     timestamp,
		Kind:        defs.MSG_BULLY_ARE_YOU_ALIVE,
	})
}

/* check the liveness of unicorn */
func startHealthCheck() {
	var count int = -1
	for {
		currentTime := getCurrentTime()
		sendHealthCheckRequestMessage(currentTime)
		var waitHealthCheckReplyTimeout chan bool = make(chan bool, 1)
		go func() {
			time.Sleep(time.Duration(TIMEOUT) * time.Millisecond)
			waitHealthCheckReplyTimeout <- true
		}()
		var i int = -1
		for i < 0 {
			select {
			/* no reply after timeout, unicorn failure detected,
			 * start election
			 */
			case <-waitHealthCheckReplyTimeout:
				close(waitHealthCheckReplyTimeout)
				fmt.Println("Time out without health check received, start election")
				if count >= 0 {
					go putUnicornUpdate(messagePasser.Message{
						Source:      localName,
						Destination: localName,
						Content:     defs.MSG_DEAD_UNICORN,
						Kind:        defs.MSG_DEAD_UNICORN,
					})
				}
				count = (count + 1) % 9
				/* No election message received yet, start an election */
				startElection()
				i = 1
			case message := <-receivedHealthCheckReplyChannel:
				/* valide health check reply message received
				 * break the inner loop, wait for TIME_BETWEEN_HEALTH_CHECK,
				 * and start another round of health check
				 */
				if message.Content == currentTime {
					// fmt.Printf("%s:\treceive health check reply from %s\n", localName, message.Source)
					for len(receivedHealthCheckReplyChannel) > 0 {
						<-receivedHealthCheckReplyChannel
					}
					i = 1
				}
			}
		}
		time.Sleep(time.Duration(TIME_BETWEEN_HEALTH_CHECK) * time.Millisecond)
	}
}

/* Start election */
func startElection() {
	currentTime := getCurrentTime()
	sendElectionMessage(currentTime)
	/* wait for answers from other nodes within timeout */
	var timeoutWaitAnswer chan bool = make(chan bool, 1)
	go func() {
		time.Sleep(time.Duration(TIMEOUT) * time.Millisecond)
		timeoutWaitAnswer <- true
	}()
	var i int = -1
	for i < 0 {
		select {
		/* no answer after timeout, the node it self is unicorn */
		case <-timeoutWaitAnswer:
			close(timeoutWaitAnswer)
			fmt.Printf("Change unicorn from %s to %s\n", unicorn, localName)
			// set self as unicorn, put an unicorn update message into unicornUpdateChannel
			go putUnicornUpdate(messagePasser.Message{
				Source:      localName,
				Destination: localName,
				Content:     localName,
				Kind:        defs.MSG_UNICORN,
			})
			unicorn = localName
			sendUnicornMessage()
			i = 1
			/* get answer within time out */
		case message := <-receivedAnswerChannel:
			/* receive a valide answer
			 * break the loop and wait for unicorn
			 */
			if message.Content == currentTime {
				for len(receivedAnswerChannel) > 0 {
					<-receivedAnswerChannel
				}
				i = 1
				var timeoutWaitUnicorn chan bool = make(chan bool, 1)
				go func() {
					time.Sleep(time.Millisecond * time.Duration(WAITING_UNICORN_MESSAGE_TIMEOUT))
					timeoutWaitUnicorn <- true
				}()
				select {
				/* no unicorn message received after timeout,
				 * start another election process
				 */
				case <-timeoutWaitUnicorn:
					close(timeoutWaitUnicorn)
					startElection()
					/* recieve an unicorn message within timeout,
					 * start health check
					 */
				case unicornMessage := <-receivedUnicornChannel:
					fmt.Printf("Change unicorn from %s to %s\n", unicorn, unicornMessage.Content)
					go putUnicornUpdate(messagePasser.Message{
						Source:      unicornMessage.Source,
						Destination: unicornMessage.Destination,
						Kind:        defs.MSG_UNICORN,
						Content:     unicornMessage.Content,
					})
					unicorn = unicornMessage.Content
				}
			}
			//otherwise, drop out-dated answer message
		}
	}
}

/*
 * Initialize the bully algorithm, and start the first election
 * @param	name
 *			the name of this node
 *
 * @param	names
 *			the names of all nodes in the group
 */
func InitBullySelection(nodes messagePasser.Nodes, name string) {
	localName = name
	frontNodes, latterNodes = getFrontAndLatterNodes(nodes, localName)
	go dispatchMessage()
	unicorn = defs.UNICORN_DEFAULT_NAME
	startHealthCheck()
}
