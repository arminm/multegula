////////////////////////////////////////////////////////////
//Multegula - PyBridge.go
//Go Bridge to Python for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package PyBridge

import (
	"os"
	"fmt"
	"net"
)

/*
 * accepts connections from Python Bridge
 * connections into connections map, after accepting
 * all connections from all other nodes in the group,
 * this routine exits

 * @param	frontNodes
 *			map that contains all nodes with smaller DNS names
 **/
func runPythonBridge() {
    ln, _ := net.Listen("tcp", 44444)
	conn, _ := ln.Accept()