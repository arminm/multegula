package main

import (
	"fmt"

	"github.com/arminm/multegula/messagePasser"
)

/*
 * get the operation, send or receive
 * @return if send, return 1; otherwise return 0
 **/
func getOperation() int {
	fmt.Println("Please select the operation you want to do, send(s)/receive(r): ")
	var operation string
	fmt.Scanf("%s", &operation)
	for operation != "s" && operation != "r" {
		fmt.Println("Please select a valid operation, send(s)/receive(r): ")
		fmt.Scanf("%s", &operation)
	}
	if operation == "s" {
		return 1
	} else {
		return 0
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
	fmt.Println("To: (ex. lunwen)")
	var destName string
	fmt.Scanf("%v", &destName)
	var destNode messagePasser.Node
	var err error
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

func main() {
	fmt.Println("initialzing message passer...")
	fmt.Println("What's the config file's name? (ex. config)")
	var configName string
	fmt.Scanf("%s", &configName)
	if len(configName) == 0 {
		configName = "config"
	}
	fmt.Println("Config Name:", configName)

	fmt.Println("Who are you? (ex. armin)")
	var nodeName string
	fmt.Scanf("%s", &nodeName)
	if len(configName) == 0 {
		configName = "armin"
	}
	fmt.Println("Node Name:", nodeName)

	messagePasser.InitMessagePasser(configName, nodeName)
	fmt.Println("message passer initialzed")

	configuration := messagePasser.Config()

	for i, node := range configuration.Nodes {
		fmt.Printf("ID: %d, Node name: %s\n", i, node.Name)
	}

	for {
		operation := getOperation()
		if operation == 1 {
			dest := getDest(configuration.Nodes)
			kind := getString("message kind")
			content := getString("message content")
			message := messagePasser.Message{Source: nodeName, Destination: dest, Content: content, Kind: kind}
			messagePasser.Send(message)
		} else {
			var message messagePasser.Message = messagePasser.Receive()
			if (message == messagePasser.Message{}) {
				fmt.Println("No messages received.")
			} else {
				fmt.Printf("Message: %+v\n", message)
			}
		}
	}
}
