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
	"time"
	"github.com/arminm/multegula/messagePasser"
	"github.com/arminm/multegula/messageType"
)

/* If a node doesn't receive message from unicorn after 
 * after this time period, it will consider the unicorn
 * is lost or crashed. After sending out an election message,
 * the node waits TIMEOUT time for answer message.
 * This time period includes the round-trip
 * transmission delay and message processing delay. It is counted
 * in millisecond.
 */
const TIMEOUT int = 200

/* The time period between two health check */
const TIME_BETWEEN_HEALTH_CHECK = 500

/* This is the time a node will wait after sending out an answer
 * message. If it receives unicorn message within this time
 * period, it will know which node is the new unicorn; otherwise,
 * it will start another election.
 */
const WAITING_UNICORN_MESSAGE_TIMEOUT int = 100

/* The name of node */
var localName string

/* The name of unicorn */
var unicorn string

/* Nodes whose names are smaller than local name in the group */
var frontNodes []string

/* Nodes whose names are greater than local name in the group */
var latterNodes []string

/* The queue for messages to be sent, messages in this queue
 * will be passed to messagePasser by mutegula
 */
var sendChannel chan messagePasser.Message = make(chan messagePasser.Message, messageType.QUEUE_SIZE)

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
	message := <-sendChannel
    return message
}

/* The queue for received messages, mutegula will put messages,
 * which come from messagePasser, into this queue
 */
var receiveChannel chan messagePasser.Message = make(chan messagePasser.Message, messageType.QUEUE_SIZE)

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
	message := <-receiveChannel
    return message
}

/* received answer message */
var receivedAnswerChannel chan messagePasser.Message = make(chan messagePasser.Message, messageType.QUEUE_SIZE)
/* received election message */
var receivedElectionChannel chan messagePasser.Message = make(chan messagePasser.Message, messageType.QUEUE_SIZE)
/* received unicorn message */
var receivedUnicornChannel chan messagePasser.Message = make(chan messagePasser.Message, messageType.QUEUE_SIZE)
/* received health check reply message */
var receivedHeadCheckReplyChannel chan messagePasser.Message = make(chan messagePasser.Message, messageType.QUEUE_SIZE)

/* dispatch received message */
func dispatchMessage() {
	for {
		message := getMessageFromReceiveChannel()
		switch message.Kind {
		case messageType.ANSWER:
			go func() {
				receivedAnswerChannel <- message
			}()
        case messageType.UNICORN:
			go func() {
				receivedUnicornChannel <- message
			}()
		case messageType.ELECTION:
			go func() {
				receivedElectionChannel <- message
			}()
        /* receive health check message, reply if node is unicorn */
        case messageType.ARE_YOU_ALIVE:
            if unicorn == localName {
                go putMessageToSendChannel(messagePasser.Message{
                    Source: localName,
                    Destination: message.Source,
                    Content: message.Content,
                    Kind: messageType.IAM_ALIVE,
                })
            }
        case messageType.IAM_ALIVE:
            go func() {
                receivedHeadCheckReplyChannel <- message
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

/* Unicorn send unicorn message to other nodes */
func sendUnicornMessage() {
	for _, name := range frontNodes {
		go putMessageToSendChannel(messagePasser.Message{
			Source: localName,
			Destination: name,
			Content: localName,
			Kind: messageType.UNICORN,
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
			Source: localName,
			Destination: name,
			Content: timestamp,
			Kind: messageType.ELECTION,
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
		Source: localName,
		Destination: destination,
		Content: timestamp,
		Kind: messageType.ANSWER,
		})
}

/* Get the string representation of current time
 * @return	the current time in string format
 */
func getCurrentTime() string {
	currentTime := time.Now()
	return currentTime.String()
}

func sendHealthCheckMessage(timestamp string) {
    go putMessageToSendChannel(messagePasser.Message{
        Source: localName,
        Destination: unicorn,
        Content: timestamp,
        Kind: messageType.ARE_YOU_ALIVE,
    })
}

/* check the liveness of unicorn */
func startHealthCheck() {
    var i int = -1
    for i < 0 {
        currentTime := getCurrentTime()
        sendHealthCheckMessage(currentTime)
        var waitHealthCheckReplyTimeout chan bool = make(chan bool, 1)
        go func(){
            time.Sleep(time.Duration(TIMEOUT) * time.Millisecond)
            waitHealthCheckReplyTimeout <- true
        }()
        var j int = -1
        for j < 0 {
            select {
            /* no reply after timeout, break loop and start election */
            case <- waitHealthCheckReplyTimeout:
                j = 1
                i = 1
                startElection()
            case message := <- receivedHeadCheckReplyChannel:
                /* valide health check reply message received
                 * break the inner loop, wait for TIME_BETWEEN_HEALTH_CHECK,
                 * and start another round of health check
                 */
                if message.Content == currentTime {
                    j = 1
                    time.Sleep(time.Duration(TIME_BETWEEN_HEALTH_CHECK) * time.Millisecond)
                }
            }
        }
    }
}

/* Start election */
func startElection() {
	currentTime := getCurrentTime()
	sendElectionMessage(currentTime)
	var timeoutWaitAnswer chan bool = make(chan bool, 1)
	go func() {
		time.Sleep(time.Duration(TIMEOUT) * time.Millisecond)
		timeoutWaitAnswer <- true
	}()
	var i int = -1
	for i < 0 {
		select {
		/* no answer after timeout */
		case <- timeoutWaitAnswer:
			close(timeoutWaitAnswer)
			unicorn = localName
			sendUnicornMessage()
			i = 1
		/* get answer within time out */
        case message := <-receivedAnswerChannel:
			/* receive an answer */
			if message.Content == currentTime {
				i = 1
				var timeoutWaitUnicorn chan bool = make(chan bool, 1)
				go func() {
					time.Sleep(time.Millisecond * time.Duration(WAITING_UNICORN_MESSAGE_TIMEOUT))
					timeoutWaitUnicorn <- true
				}()
				select {
				case <- timeoutWaitUnicorn:
					startElection()
				case <- receivedUnicornChannel:
					unicorn = localName
					startHealthCheck()
				}
			}
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
func InitBullySelection(name string, names []string) {
	localName = name
	frontNodes, latterNodes = getFrontAndLatterNodes(names, localName)
	dispatchMessage()
	//TODO start the first election
}
