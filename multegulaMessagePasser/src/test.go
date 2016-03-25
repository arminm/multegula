package main

import (
	"encoding/json"
	"fmt"
	"bufio"
	"os"
	"sort"
	"messagePasser"
)

func func main() {
	fmt.Println("initialzing message passer...")
	//messagePasser.InitMessagePasser()
	fmt.Println("message passer initialzed")

	file, _ := os.Open("config.json")
	decoder := json.NewDecoder(file)
	configuration := messagePasser.Configuration{}
	err := decoder.Decode(&configuration)
	if err != nil {
	  fmt.Println("error:", err)
	}

	sort(configuration.group)
	fmt.Println("local name: " + configuration.localName)
	for i, dns := range configuration.group {
		fmg.Printf("ID %d, DNS name %s\n", i, dns)
	}
}
