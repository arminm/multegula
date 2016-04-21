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
	"time"
    "fmt"
	"github.com/arminm/multegula/messagePasser"
	"github.com/arminm/multegula/defs"
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

/* The queue for messages to be sent, messages in this queue
 * will be passed to messagePasser by mutegula
 */
var sendChannel chan messagePasser.Message = make(chan messagePasser.Message, defs.QUEUE_SIZE)

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
 * @return	the message got from sendhannel
 */
func GetMessageFromSendChannel() messagePasser.Message {
	message := <- sendChannel
    return message
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
	receiveChannel <- message
}

/*
 * Get message from receiveChannel
 * @return	the message got from receiveChannel
 */
func getMessageFromReceiveChannel() messagePasser.Message {
	message := <- receiveChannel
    return message
}

/* received answer message */
var receivedAnswerChannel chan messagePasser.Message = make(chan messagePasser.Message, defs.QUEUE_SIZE)
/* received unicorn message */
var receivedUnicornChannel chan messagePasser.Message = make(chan messagePasser.Message, defs.QUEUE_SIZE)
/* received health check reply message */
var receivedHealthCheckReplyChannel chan messagePasser.Message = make(chan messagePasser.Message, defs.QUEUE_SIZE)

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
                Source: localName,
                Destination: message.Source,
                Content: message.Content,
                Kind: defs.MSG_BULLY_IAM_ALIVE,
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
			Kind: defs.MSG_BULLY_UNICORN,
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
			Kind: defs.MSG_BULLY_ELECTION,
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
		Kind: defs.MSG_BULLY_ANSWER,
		})
}

/* Get the string representation of current time
 * @return	the current time in string format
 */
func getCurrentTime() string {
	currentTime := time.Now()
	return currentTime.String()
}

func sendHealthCheckRequestMessage(timestamp string) {
    go putMessageToSendChannel(messagePasser.Message{
        Source: localName,
        Destination: unicorn,
        Content: timestamp,
        Kind: defs.MSG_BULLY_ARE_YOU_ALIVE,
    })
}

/* check the liveness of unicorn */
func startHealthCheck() {
    for {
        currentTime := getCurrentTime()
        sendHealthCheckRequestMessage(currentTime)
        var waitHealthCheckReplyTimeout chan bool = make(chan bool, 1)
        go func(){
            time.Sleep(time.Duration(TIMEOUT) * time.Millisecond)
            waitHealthCheckReplyTimeout <- true
        }()
        var i int = -1
        for i < 0 {
            select {
            /* no reply after timeout, unicorn failure detected,
             * start election
             */
            case <- waitHealthCheckReplyTimeout:
                close(waitHealthCheckReplyTimeout)
                fmt.Println("Time out without health check received, start election")
                /* No election message received yet, start an election */
                startElection()
                i = 1
            case message := <- receivedHealthCheckReplyChannel:
                /* valide health check reply message received
                 * break the inner loop, wait for TIME_BETWEEN_HEALTH_CHECK,
                 * and start another round of health check
                 */
                if message.Content == currentTime {
                    fmt.Printf("Valide health check reply: %s %s\n", message.Source, message.Content)
                    for len(receivedHealthCheckReplyChannel) > 0 {
                        <- receivedHealthCheckReplyChannel
                    }
                    i = 1
                } else {// otherwise, drop out-dated health check reply
                    fmt.Printf("Invalid health check reply from %s at %s\n", message.Source, getCurrentTime())
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
		case <- timeoutWaitAnswer:
            fmt.Println("Time out without answer received")
			close(timeoutWaitAnswer)
            fmt.Printf("Change unicorn from %s to %s\n", unicorn, localName)
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
                    <- receivedAnswerChannel
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
				case <- timeoutWaitUnicorn:
                    close(timeoutWaitUnicorn)
					startElection()
				/* recieve an unicorn message within timeout,
				 * start health check
				 */
                case unicornMessage := <- receivedUnicornChannel:
                    fmt.Printf("Change unicorn from %s to %s\n", unicorn, unicornMessage.Content)
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
func InitBullySelection(name string, names []string) {
	localName = name
	frontNodes, latterNodes = getFrontAndLatterNodes(names, localName)
	go dispatchMessage()
    unicorn = defs.UNICORN_DEFAULT_NAME
    startHealthCheck()
}
