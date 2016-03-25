package main

import (
	"encoding/json"
	"fmt"
    "os"
    "sort"
    "messagePasser"
)


func main() {
	fmt.Println("initialzing message passer...")
	messagePasser.InitMessagePasser()
	fmt.Println("message passer initialzed")

	file, _ := os.Open("config.json")
	decoder := json.NewDecoder(file)
	configuration := messagePasser.Configuration{}
	err := decoder.Decode(&configuration)
	if err != nil {
	  fmt.Println("error:", err)
	}

    fmt.Println(configuration)

	sort.Strings(configuration.Group)
	fmt.Println("local name: " + configuration.LocalName[0])
	for i, dns := range configuration.Group {
		fmt.Printf("ID %d, DNS name %s\n", i, dns)
	}
}
