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
 * get DNS ID
 * @param n
 *        the number of DNS ID
 *
 * @return selected DNS ID
 **/
func getNodeID(n int) int {
	fmt.Println("Please choose one Node ID: ")
	var id int
	fmt.Scanf("%d", &id)
	for id < 0 || id >= n {
		fmt.Println("Invalid Node ID, please select again: ")
		fmt.Scanf("%d", &id)
	}
	return id
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
	for len(res) == 0 {
		fmt.Println("string cannot be empty, please input again:")
		fmt.Scanf("%s", &res)
	}
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
			id := getNodeID(len(configuration.Nodes))
			kind := getString("message kind")
			content := getString("message content")
			message := messagePasser.Message{Source: nodeName, Destination: configuration.Nodes[id].Name, Content: content, Kind: kind}
			messagePasser.Send(message)
		} else {
			var message messagePasser.Message = messagePasser.Receive()
			if (message == messagePasser.Message{}) {
				fmt.Println("No messages received.")
			} else {
				fmt.Println("Message comes from: " + message.Source)
				fmt.Println("Message goes to: " + message.Destination)
				fmt.Println("Message content: " + message.Content)
				fmt.Println("Message kind: " + message.Kind)
			}
		}
	}
}
