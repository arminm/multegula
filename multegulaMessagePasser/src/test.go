package main

import (
	"encoding/json"
	"fmt"
    "os"
    "sort"
)

//Config Reading Example
type Configuration struct {
    bootstrapServer  []string
    localName []string
    group []string
}

func main() {
/*	fmt.Println("initialzing message passer...")
	messagePasser.InitMessagePasser()
	fmt.Println("message passer initialzed")*/

	file, _ := os.Open("config.json")
	decoder := json.NewDecoder(file)
	configuration := Configuration{}
	err := decoder.Decode(&configuration)
	if err != nil {
	  fmt.Println("error:", err)
	}

    fmt.Println(configuration)

	sort.Strings(configuration.group)
//	fmt.Println("local name: " + configuration.localName[0])
	for i, dns := range configuration.group {
		fmt.Printf("ID %d, DNS name %s\n", i, dns)
	}
}
