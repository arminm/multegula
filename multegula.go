////////////////////////////////////////////////////////////
//Multegula - multegula.go
//Main Go Package for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package main

import (
	"flag"
	"fmt"
//	"reflect"
	"strconv"
	"github.com/arminm/multegula/bridges"
	"github.com/arminm/multegula/messagePasser"
	"github.com/arminm/multegula/messageType"
	"github.com/arminm/multegula/bullySelection"
)


/*** MESSAGE TYPE CONSTANTS ***/
const MSG_GAME_TYPE 	string = "MSG_GAME_TYPE"
const MSG_MYNAME 		string = "MSG_MYNAME"
const MSG_PADDLE_POS 	string = "MSG_PADDLE_POS"
const MSG_PADDLE_DIR 	string = "MSG_PADDLE_DIR"

/*** MESSAGE DESTINATION CONSTANTS ***/
const MULTICAST_DEST string = "EVERYBODY"
const MULTEGULA_DEST string = "MULTEGULA"

/*** MESSAGE SOURCE CONTENTS ***/
const UI_SOURCE string = "UI"

/*** MESSAGE PAYLOAD CONSTANTS ***/
const GAME_TYPE_MULTI 	string = "MULTI"
const GAME_TYPE_SINGLE	string = "SINGLE"

/* 
 * This is the sendChannel for message dispatcher.
 * Any components like UI or bully algorithm will
 * put messages into this channel if they whan to
 * send message out. Message dispatcher will get
 * messages out from this channel and send them
 * to messagePasser
 */
var sendChannel chan messagePasser.Message = make(chan messagePasser.Message, messageType.QUEUE_SIZE)

/*
 * get message out from sendChannel
 * @return the message got from sendChannel
 */
func getMessageFromSendChannel() messagePasser.Message {
	message := <- sendChannel
	return message
}

/*
 * put message into sendChannel
 * @param message - message to be put into sendChannel
 */
func putMessageIntoSendChannel(message messagePasser.Message) {
	sendChannel <- message
}

/*
 * get the operation, send or receive
 * @return if send, return 1; otherwise return 0
 **/
func getOperation() int {
	var operation string
	for {
		fmt.Println("Send(s) / Receive(r) / Multicast (m): ")
		fmt.Scanf("%s", &operation)
		switch operation {
		case "s":
			return 0
		case "r":
			return 1
		case "m":
			return 2
		default:
			fmt.Printf("'%v' is Invalid. Please select a valid operation.", operation)
		}
	}
}

/*
 * get destination name
 * @param nodes
 *        the available nodes to contact
 *
 * @return destination name string
 **/
func getDest(nodes []messagePasser.Node) string {
	fmt.Println("To: (ex. lunwen OR 1)")
	var destName string
	fmt.Scanf("%v", &destName)
	// Check if input is an ID
	id, err := strconv.Atoi(destName)
	if err == nil && id >= 0 && id < len(nodes) {
		return nodes[id].Name
	}
	// else input must be a name
	var destNode messagePasser.Node
	for len(destName) > 0 {
		_, destNode, err = messagePasser.FindNodeByName(nodes, destName)
		if err == nil {
			break
		}
		fmt.Printf("Couldn't find '%v', please try again:\n", destName)
		fmt.Scanf("%v", &destName)
	}

	return destNode.Name
}

/*
 * get string from stdin
 * @param stringType
 *        the type of string: message content or message kind
 *
 * @return string got from stdin
 **/
func getString(stringType string) string {
	fmt.Println("Please input " + stringType + ":")
	var res string
	fmt.Scanf("%s", &res)
	return res
}

/*
 * Prompts the user for the configuration file's name
 * @return configuration file's name string
 */
func getConfigName() string {
	var configName string
	fmt.Println("What's the config file's name? (ex. config)")
	fmt.Scanf("%s", &configName)
	if len(configName) == 0 {
		configName = "config" // default name
	}
	return configName
}

/*
 * Prompts the user for the local Node's name
 * @return local Node's name string
 */
func getLocalName() string {
	var localName string
	fmt.Println("Who are you? (ex. armin)")
	fmt.Scanf("%s", &localName)
	if len(localName) == 0 {
		localName = "unknown" // default name
	}
	return localName
}

/*
 * prompts the user and builds a message
 */
func getMessage(nodes []messagePasser.Node, localNodeName string) messagePasser.Message {
	dest := getDest(nodes)
	kind := getString("message kind")
	content := getString("message content")
	return messagePasser.Message{Source: localNodeName, Destination: dest, Content: content, Kind: kind}
}

/*
 * retreives local name from the UI
 */
func uiGetLocalName() (localName string) {
	for {
		message := bridges.ReceiveFromPyBridge()
		if message.Kind == MSG_MYNAME {
			localName = message.Content
			break
		}
	}
	return localName
}

/*
 * retreives game type from the UI
 */
func uiGetGameType() (gameType string) {
	for {
		message := bridges.ReceiveFromPyBridge()
		if message.Kind == MSG_GAME_TYPE {
			gameType = message.Content
			break
		}
	}
	return gameType	
}

/* wait for incoming messages from the UI */
func PyBridgeReceiver() {
	for {
		message := bridges.ReceiveFromPyBridge()
        go putMessageIntoSendChannel(message)
	}
}

/* wait for incoming messages from the bully algorithm */
func BullyReceiver() {
	for {
		message := bullySelection.GetMessageFromSendChannel()
		go putMessageIntoSendChannel(message)
	}
}

/* receive message from messagePasser and route to correct location */
func inboundDispatcher() {
	for {
		// get message from MessagePasser
		message := messagePasser.Receive()

		// Based on the type of message, determine where it needs routed
		switch message.Kind {
		case MSG_PADDLE_POS:
			bridges.SendToPyBridge(message)
		case MSG_PADDLE_DIR:
			bridges.SendToPyBridge(message)
		case messageType.ELECTION:
			bullySelection.PutMessageToReceiveChannel(message)
		case messageType.ANSWER:
			bullySelection.PutMessageToReceiveChannel(message)
		case messageType.UNICORN:
			bullySelection.PutMessageToReceiveChannel(message)
		case messageType.ARE_YOU_ALIVE:
			bullySelection.PutMessageToReceiveChannel(message)
		case messageType.IAM_ALIVE:
			bullySelection.PutMessageToReceiveChannel(message)
		}
	}
}

/* Handles all outbound messages  */
func outboundDispatcher() {
	for {
		// get message from the send channel
		message := getMessageFromSendChannel()

		// based on it's destination, determine which messagePasser
		//	routine is appropriate
		if message.Destination == MULTICAST_DEST {
			messagePasser.Multicast(&message)
		} else {
			messagePasser.Send(message)
		}
	}
}

/*
 * parses main arguments passed in through command-line
 */
func parseMainArguments(args []string) (configName string, localNodeName string) {

	if len(args) > 0 {
		configName = args[0]
	} else {
		configName = getConfigName()
	}
	fmt.Println("Config Name:", configName)

	if len(args) > 1 {
		localNodeName = args[1]
	} else {
		localNodeName = getLocalName()
	}
	fmt.Println("Local Node Name:", localNodeName)
	return configName, localNodeName
}

func skinnyParseMainArguments(args []string) (configName string) {

	if len(args) > 0 {
		configName = args[0]
	} else {
		configName = getConfigName()
	}
	fmt.Println("Config Name:", configName)
	return configName
}

/* the Main function of the Multegula application */
func main() {
//	testFlag := flag.Bool("test", false, "Test Mode Flag")
	testFlag := flag.Bool("test", true, "Test Mode Flag")
	portFlag := flag.Int("port", 44444, "Local port number for Python-Go bridge.")
	flag.Parse()
	// Read command-line arguments and prompt the user if not provided
	args := flag.Args()

	if *testFlag {
		configName, localNodeName := parseMainArguments(args)
		fmt.Print("--------------------------------\n")
		fmt.Println("Initing with localName:", localNodeName)
		messagePasser.InitMessagePasser(configName, localNodeName)

		configuration := messagePasser.Config()
		fmt.Println("Available Nodes:")
		for id, node := range configuration.Nodes {
			fmt.Printf("  ID:%d – %s\n", id, node.Name)
		}
		/* start a receiveRoutine to be able to use nonBlockingReceive */
	//	go receiveRoutine()
		go BullyReceiver()
		go inboundDispatcher()
        /* start bully algorithm */
        go bullySelection.InitBullySelection(localNodeName, messagePasser.GetNodeNames())
		outboundDispatcher()

/*		fmt.Println("Please select the operation you want to do:")
		for {
			fmt.Println("Getting operation")
			operation := getOperation()
			if operation == 0 {
				message := getMessage(configuration.Nodes, localNodeName)
				messagePasser.Send(message)
			} else if operation == 1 {
				var message messagePasser.Message = nonBlockingReceive()
				if (reflect.DeepEqual(message, messagePasser.Message{})) {
					fmt.Print("No messages received.\n\n")
				} else {
					fmt.Printf("Received: %+v\n\n", message)
				}
			} else if operation == 2 {
				message := getMessage(configuration.Nodes, localNodeName)
				messagePasser.Multicast(&message)
				fmt.Println("Did multicast")
			} else {
				fmt.Println("Operation not recognized. Please try again.")
			}
		}*/
	} else {
		/**** THIS IS LIKE ACTUAL GAMEPLAY ***/
		// initialize communication with the UI
		fmt.Printf("Port is:%d\n", *portFlag)
		bridges.InitPyBridge(*portFlag)

		// get the localname
		localNodeName := uiGetLocalName()
		fmt.Println("My name is:", localNodeName)

		// determine the game type (multi or single player)
		gameType := uiGetGameType()

		if gameType == GAME_TYPE_MULTI {
			configName := skinnyParseMainArguments(args)
			messagePasser.InitMessagePasser(configName, localNodeName)

			/* start the routine waiting for messages coming from UI */
			go PyBridgeReceiver()
			go BullyReceiver()
			go inboundDispatcher()
            /* start bully algorithm */
            go bullySelection.InitBullySelection(localNodeName, messagePasser.GetNodeNames())
			outboundDispatcher()
		}
	}
}

/* testing functions */
var receiveQueue = []messagePasser.Message{}

func receiveRoutine() {
	for {
		messagePasser.Push(&receiveQueue, messagePasser.Receive())
	}
}

func nonBlockingReceive() messagePasser.Message {
	return messagePasser.Pop(&receiveQueue)
}
