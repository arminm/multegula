package main

import (
	"encoding/json"
	"fmt"
    "os"
    "sort"
    "./multegula/messagePasser"
    "strconv"
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
    if(operation == "s") {
        return 1
    } else {
        return 0
    }
}

/*
 * print out available DNS IDs
 * @param n
 *        number of DNS IDs
 **/
func printDNSID(n int) {
    fmt.Println("Valid operation ID: ")
    for i := 0; i < n; i++ {
        fmt.Println("\t" + strconv.Itoa(i))
    }
}

/*
 * get DNS ID
 * @param n
 *        the number of DNS ID
 *
 * @return selected DNS ID
 **/
func getDNSID(n int) int {
    printDNSID(n)
    fmt.Println("Please choose one DNS ID: ")
    var id int
    fmt.Scanf("%d", &id)
    for id < 0 || id >= n {
        fmt.Println("Invalid DNS ID, please select again: ")
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
	messagePasser.InitMessagePasser()
	fmt.Println("message passer initialzed")

	file, _ := os.Open("./messagePasser/config.json")
	decoder := json.NewDecoder(file)
	configuration := messagePasser.Configuration{}
	err := decoder.Decode(&configuration)
	if err != nil {
	  fmt.Println("error:", err)
	}

	sort.Strings(configuration.Group)

	fmt.Println("local name: " + configuration.LocalName[0])
	for i, dns := range configuration.Group {
		fmt.Printf("ID %d, DNS name %s\n", i, dns)
	}

    for {
        operation := getOperation()
        if(operation == 1) {
            id := getDNSID(len(configuration.Group))
            kind := getString("message kind")
            content := getString("message content")
            message := messagePasser.Message{Source: configuration.LocalName[0], Destination: configuration.Group[id], Content: content, Kind: kind}
            messagePasser.Send(message)
        } else {
            var message messagePasser.Message = messagePasser.Receive()
            if(message == messagePasser.Message{}) {
                fmt.Println("There is no message received right now.")
            } else {
                fmt.Println("Message comes from: " + message.Source)
                fmt.Println("Message goes to: " + message.Destination)
                fmt.Println("Message content: " + message.Content)
                fmt.Println("Message kind: " + message.Content)
            }
        }
    }
}
