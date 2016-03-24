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
//	"net"
//	"bufio"
	"sort"
)

//Config Reading Example
type Configuration struct {
    BootstrapServer  []string
    LocalName []string
    Group []string
}

/* map stores connections to each node
 * <key, value> = <dns, connection>
 **/
var connections map[string]Conn = make(map[string]Conn)

/* port number for TCP connection */
const port string = ":8081"

/* 
 * accepts connections from other nodes and stores 
 * connections into connections map
 * @param	group
 *			the DNS name of each node in the group
 * 
 * @param	localName
 *			the DNS name of local node
 **/
func acceptConnection(group []string, sring localName) {
	
}

/*
 * send connections to nodes with greater DNS names
 * and stores connections into connections map
 * @param	group
 *			the DNS name of each node in the group
 *
 * @param	localName
 *			the DNS name of local node
 **/
func sendConnection(group []string, string localName) {
	
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
	fmt.Println(configuration.LocalName) // output: [local.dyndns.org]
	fmt.Println(configuration.Group) // output: [local.dyndns.org node1.dyndns.org node2.dyndns.org]

	/* sort group's dns name, node only sends TCP connection to nodes
	 * which are greater in the sorted order so that there is only one
	 * TCP connection between each other
	 **/
	sort.Strings(configuration.Group)
}

