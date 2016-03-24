////////////////////////////////////////////////////////////
//Multegula - MessagePasser.go 
//Multicasting Message Passer for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package main

import (
	"encoding/json"
	"os"
	"fmt"
	"net"
	"bufio"
)

//Config Reading Example
type Configuration struct {
    BootstrapServer  []string
    LocalName []string
    Group []string
}

func main(){
	file, _ := os.Open("config.json")
	decoder := json.NewDecoder(file)
	configuration := Configuration{}
	err := decoder.Decode(&configuration)
	if err != nil {
	  fmt.Println("error:", err)
	}
	fmt.Println(configuration.BootstrapServer) // output: [BootstrapServer]
	fmt.Println(configuration.LocalName)
	fmt.Println(configuration.Group)

	bootstrapServerDNS := configuration.BootstrapServer[0]
	/* setup a connection to BootstrapServer and get the IPs of group */
	conn, _ := net.Dial("tcp", bootstrapServerDNS);
	
}

