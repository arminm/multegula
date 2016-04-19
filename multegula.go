////////////////////////////////////////////////////////////
//Multegula - multegula.go
//Main Go Package for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package main

import (
	"flag"
	"fmt"
	"reflect"
	"sort"
	"strconv"
	"github.com/arminm/multegula/bootstrapClient"
	"github.com/arminm/multegula/bridges"
	"github.com/arminm/multegula/defs"
	"github.com/arminm/multegula/messagePasser"
	"github.com/arminm/multegula/bullySelection"
)

/*
 * This is the sendChannel for message dispatcher.
 * Any components like UI or bully algorithm will
 * put messages into this channel if they whan to
 * send message out. Message dispatcher will get
 * messages out from this channel and send them
 * to messagePasser
 */
var sendChannel chan messagePasser.Message = make(chan messagePasser.Message, defs.QUEUE_SIZE)

/*
 * get message out from sendChannel
 * @return the message got from sendChannel
 */
func getMessageFromSendChannel() messagePasser.Message {
	message := <-sendChannel
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
		if message.Kind == defs.MSG_MYNAME {
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
		if message.Kind == defs.MSG_GAME_TYPE {
			gameType = message.Content
			break
		}
	}
	return gameType
}

/* 
 * sets the orientation of the players to alphabetical
 */
func uiSetCompetitorLocation(myName string, peers *[]messagePasser.Node) {
	var toSend messagePasser.Message;
	var nodeNames = []string{};

	// loop through all nodes and pull out names
	for _, node := range *peers {
		nodeNames = append(nodeNames, node.Name);
	}

	// sort and get length
	sort.Strings(nodeNames);
	length := len(nodeNames);

	// create content of message
	content := fmt.Sprintf("%d", length);
	for _, name := range nodeNames {
		content = fmt.Sprintf("%v%v%v", content, defs.PAYLOAD_DELIMITER, name)
	}

	// create message and send message
	toSend.Source = myName;
	toSend.Destination = myName;
	toSend.Kind = defs.MSG_PLAYER_LOC;
	toSend.Content = content;
	bridges.SendToPyBridge(toSend);
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
		case defs.MSG_PADDLE_POS:
			bridges.SendToPyBridge(message)
		case defs.MSG_PADDLE_DIR:
			bridges.SendToPyBridge(message)
		case defs.MSG_BALL_MISSED:
			bridges.SendToPyBridge(message)
		case defs.MSG_BALL_DEFLECTED:
			bridges.SendToPyBridge(message)
		case defs.MSG_BLOCK_BROKEN:
			bridges.SendToPyBridge(message)
		case defs.ELECTION:
			bullySelection.PutMessageToReceiveChannel(message)
		case defs.ANSWER:
			bullySelection.PutMessageToReceiveChannel(message)
		case defs.UNICORN:
			bullySelection.PutMessageToReceiveChannel(message)
		case defs.ARE_YOU_ALIVE:
			bullySelection.PutMessageToReceiveChannel(message)
		case defs.IAM_ALIVE:
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
		if message.Destination == defs.MULTICAST_DEST {
			messagePasser.Multicast(&message)
		} else {
			messagePasser.Send(message)
		}
	}
}

/*
 * parses main arguments passed in through command-line
 */
func parseMainArguments(args []string) string {
	var localNodeName string
	if len(args) > 0 {
		localNodeName = args[1]
	} else {
		localNodeName = getLocalName()
	}
	fmt.Println("Local Node Name:", localNodeName)
	return localNodeName
}

/* the Main function of the Multegula application */
func main() {
	testFlag := flag.Bool("test", false, "Test Mode Flag")
	bootstrapTestFlag := flag.Bool("bt", false, "Bootstrap Test Mode Flag")
	uiPortFlag := flag.Int("uiport", defs.DEFAULT_UI_PORT, "Local port number for Python-Go bridge.")
	gamePortFlag := flag.Int("gameport", defs.DEFAULT_GAME_PORT, "Local port number for MessagePasser.")
	flag.Parse()
	// Read command-line arguments and prompt the user if not provided
	args := flag.Args()

	// nodes used for testing purposes only
	nodes := []messagePasser.Node{messagePasser.Node{Name: "armin", IP: "127.0.0.1", Port: 10011, DNS: "none"}, messagePasser.Node{Name: "garrett", IP: "127.0.0.1", Port: 10012, DNS: "none"}, messagePasser.Node{Name: "lunwen", IP: "127.0.0.1", Port: 10013, DNS: "none"}, messagePasser.Node{Name: "daniel", IP: "127.0.0.1", Port: 10014, DNS: "none"}}

	// for testing the bootstrapping
	if *bootstrapTestFlag {
		localName := getLocalName()
		_, localNode, _ := messagePasser.FindNodeByName(nodes, localName)
		fmt.Println("[MULTEGULA CORE] Contacting the bootstrap server...")
		peers, err := bootstrapClient.GetNodes(localNode)
		if err != nil {
			fmt.Println("Got error:", err)
		} else {
			fmt.Printf("Got peers: %+v\n", peers)
		}
		return
	}

	if *testFlag {
		localNodeName := parseMainArguments(args)

		fmt.Print("--------------------------------\n")
		fmt.Println("Initing with localName:", localNodeName)
		messagePasser.InitMessagePasser(nodes, localNodeName)

		fmt.Println("Available Nodes:")
		for id, node := range nodes {
			fmt.Printf("  ID:%d – %s\n", id, node.Name)
		}
		/* start a receiveRoutine to be able to use nonBlockingReceive */
		go receiveRoutine()

		fmt.Println("Please select the operation you want to do:")
		for {
			fmt.Println("Getting operation")
			operation := getOperation()
			if operation == 0 {
				message := getMessage(nodes, localNodeName)
				messagePasser.Send(message)
			} else if operation == 1 {
				var message messagePasser.Message = nonBlockingReceive()
				if (reflect.DeepEqual(message, messagePasser.Message{})) {
					fmt.Print("No messages received.\n\n")
				} else {
					fmt.Printf("Received: %+v\n\n", message)
				}
			} else if operation == 2 {
				message := getMessage(nodes, localNodeName)
				messagePasser.Multicast(&message)
				fmt.Println("Did multicast")
			} else {
				fmt.Println("Operation not recognized. Please try again.")
			}
		}
	}

	/**** THIS IS LIKE ACTUAL GAMEPLAY ***/
	// initialize communication with the UI
	fmt.Printf("[MULTEGULA CORE] UI Port flag is: %d\n", *uiPortFlag)
	bridges.InitPyBridge(*uiPortFlag)

	// get the localname
	localNodeName := uiGetLocalName()
	fmt.Println("[MULTEGULA CORE] My name is:", localNodeName)

	// determine the game type (multi or single player)
	gameType := uiGetGameType()

	if gameType == defs.GAME_TYPE_MULTI {
		// get fellow players
		localNode := messagePasser.Node{Name: localNodeName, IP: "127.0.0.1", Port: *gamePortFlag, DNS: ""}
		peers, err := bootstrapClient.GetNodes(localNode)
		if err != nil {
			fmt.Println("[MULTEGULA CORE] Couldn't get peers:", err)
			panic(err)
		}
		*peers = append(*peers, localNode)

		// set competitor location
		uiSetCompetitorLocation(localNode.Name, peers)

		// initialize message passer
		messagePasser.InitMessagePasser(*peers, localNodeName)
		fmt.Println(localNodeName, "[MULTEGULA CORE] Made messagepasser.")

		/* start the routine waiting for messages coming from UI */
		go PyBridgeReceiver()
		go BullyReceiver()
		go inboundDispatcher()
		outboundDispatcher()
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
