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

/* map stores connections to each node
 * <key, value> = <dns, connection>
 **/
var connections map[string]Conn = make(map[string]Conn)

/* port number for TCP connection */
const port string = ":8081"

/*
 * separate nodes' DNS name into two parts based on lexicographical order
 * @param	group
 *			the DNS name of each node in the group
 *
 * @param	localName
 *			the DNS name of local node
 * 
 * @return	frontNodes
 *			nodes smaller than localName
 *			latterNodes
 *			nodes greater than localName
 **/
func getFrontAndLatterNodes(group []string, localName string) (map[string]bool, map[string]bool) {
	var frontNodes map[string]bool = make(map[string]bool)
	var latterNodes map[string]bool = make(map[string]bool)
	for _, dns := range group {
		if(dns < localName) {
			frontNodes[dns] = true
		} else if(dns > localName) {
			latterNodes[dns] = true
		}
	}
	return frontNodes, latterNodes
}


/* 
 * accepts connections from other nodes and stores 
 * connections into connections map, after accepting
 * all connections from all other nodes in the group,
 * this routine exits
 **/
func acceptConnection(frontNodes map[string]bool) {
	fmt.Println("Accepting connections...")
	ln, _ = net.Listen("tcp", port)
	for len(frontNodes) > 0 {
		/* 
		 * when a node first connects to other nodes, it will first 
		 * send it's DNS name so that another node can know it
		 **/
		conn, _ := ln.Accept()
		dns, _ := bufio.NewReader(conn).ReadString('\n')
		fmt.Println("Received connection from " + dns)
		delete(frontNodes, dns)
		connections[dns] = conn
	}
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

	frontNodes, latterNodes := getFrontAndLatterNodes(configuration.Group, configuration.LocalName[0])
	fmt.Println(frontNodes)
	fmt.Println(latterNodes)
}

