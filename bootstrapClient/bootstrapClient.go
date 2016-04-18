////////////////////////////////////////////////////////////
//Multegula - BootstrapClient.go
//Bootstrapping/Grouping Client for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package bootstrapClient

import (
	"encoding/gob"
	"fmt"
	"net"
	"time"

	"github.com/arminm/multegula/messagePasser"
)

const SERVER_DNS string = "multegula.dyndns.org:55555"

// const SERVER_DNS string = "127.0.0.1:55555"

/*
 * Get Nodes
 *
 **/
func GetNodes(localNode messagePasser.Node) (*[]messagePasser.Node, error) {
	var conn net.Conn
	var err error
	for {
		//TODO: Make this configurable
		conn, err = net.Dial("tcp", SERVER_DNS)
		if err == nil {
			break
		}
		fmt.Print(".")
		time.Sleep(time.Second * 1)
	}
	fmt.Println("Connected to Bootstrap Server!")
	sendNode(localNode, conn)
	fmt.Println("Sent local info. Waiting for peer nodes...")
	return receiveNodes(conn)
}

/*
 * Send Nodes to Bootstrap Server
 *
 *
 **/
func sendNode(node messagePasser.Node, conn net.Conn) {
	encoder := gob.NewEncoder(conn)
	encoder.Encode(node)
}

/*
 * Receive Nodes from Bootstrap Server
 *
 **/
func receiveNodes(conn net.Conn) (*[]messagePasser.Node, error) {
	dec := gob.NewDecoder(conn)
	nodes := &[]messagePasser.Node{}
	err := dec.Decode(nodes)
	if err != nil {
		return nodes, err
	}
	return nodes, nil
}
