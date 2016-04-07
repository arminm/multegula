package main

import (
	"fmt"
	"os"
	"strconv"
	"github.com/arminm/multegula/messagePasser"
	"github.com/arminm/multegula/bridges"
)

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
		destNode, err = messagePasser.FindNodeByName(nodes, destName)
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

func main() {
	// Read command-line arguments and prompt the user if not provided
	args := os.Args[1:]

	var configName string
	if len(args) > 0 {
		configName = args[0]
	} else {
		configName = getConfigName()
	}
	fmt.Println("Config Name:", configName)

	var localNodeName string
	if len(args) > 1 {
		localNodeName = args[1]
	} else {
		localNodeName = getLocalName()
	}
	fmt.Println("Local Node Name:", localNodeName)
    bridges.InitPyBridge(configName, localNodeName)
/*	messagePasser.InitMessagePasser(configName, localNodeName)

	fmt.Print("--------------------------------\n")

	configuration := messagePasser.Config()
	fmt.Println("Available Nodes:")
	for id, node := range configuration.Nodes {
		fmt.Printf("  ID:%d – %s\n", id, node.Name)
	}

	fmt.Println("Please select the operation you want to do:")
	for {
		operation := getOperation()
		if operation == 0 {
			message := getMessage(configuration.Nodes, localNodeName)
			messagePasser.Send(message)
		} else if operation == 1 {
			var message messagePasser.Message = messagePasser.Receive()
			if (message == messagePasser.Message{}) {
				fmt.Print("No messages received.\n\n")
			} else {
				fmt.Printf("Received: %+v\n\n", message)
			}
		} else if operation == 2 {
			message := getMessage(configuration.Nodes, localNodeName)
			messagePasser.Multicast(&message)
		} else {
			fmt.Println("Operation not recognized. Please try again.")
		}
	}*/
}
