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
	"strconv"
	"strings"
	"github.com/arminm/multegula/bridges"
	"github.com/arminm/multegula/messagePasser"
)

// constants
const UI_MULTICAST_DEST string = "EVERYBODY"
const UI_MULTEGULA_DEST string = "MULTEGULA"
const MSG_MYNAME string = "MSG_MYNAME"

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
		if strings.EqualFold(message.Kind, MSG_MYNAME) {
			localName = message.Content
			break
		}
	}
	return localName
}

/* receive message from PyBridge and send to messagePasser */
func uiReceiveAndReact() {
	for {
		message := bridges.ReceiveFromPyBridge()

		//fmt.Println("Multegula: UI message received - ", message)
		if strings.EqualFold(message.Destination, UI_MULTICAST_DEST) {
			messagePasser.Multicast(&message)
		} else if strings.EqualFold(message.Destination, UI_MULTEGULA_DEST) {
			fmt.Println("TODO: Handle any messages meant only for Multegula.")
		} else {
			fmt.Println("TODO: Handle any messages from the UI that have invalid destinations")
		}		
	}

}


/* receive message from PyBridge and send to messagePasser */
func networkReceiveAndReact() {
	for {
		message := messagePasser.Receive()
		//fmt.Println("Multegula: received network message -", message)
		switch message.Kind {
		case "MSG_PADDLE_POS":
			bridges.SendToPyBridge(message)
		case "MSG_PADDLE_DIR":
			bridges.SendToPyBridge(message)
		}
	}
}

/* receive message from MessagePasser and send to PyBridge */
func pyBridgeSend() {
	for {
		message := messagePasser.Receive()
		bridges.SendToPyBridge(message)
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
	testFlag := flag.Bool("test", false, "Test Mode Flag")
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
		go receiveRoutine()

		fmt.Println("Please select the operation you want to do:")
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
		}
	} else {
		configName := skinnyParseMainArguments(args)

		// get the the local node name from the UI
		// NOTE: this will be required when we move to the bootstrap server method, for now
		//	this must match the config file.
		fmt.Printf("Port is:%d\n", *portFlag)
		bridges.InitPyBridge(*portFlag)
		localNodeName := uiGetLocalName()
		fmt.Println("Multegula: GOT NAME FROM UI:", localNodeName)
		messagePasser.InitMessagePasser(configName, localNodeName)
		fmt.Println("Multegula: made message passer for", localNodeName)
		// main loop - this runs the Multegula in all it's glory

		go uiReceiveAndReact()
		go networkReceiveAndReact()

		for {
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
