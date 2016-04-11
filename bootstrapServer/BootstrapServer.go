////////////////////////////////////////////////////////////
//Multegula - BootstrapServer.go
//Bootstrapping/Grouping Server for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package main

import (
    "fmt"
    "log"
    "net"
)

//Listen on port 55555 for inbound connections
const listenAddr = "localhost:55555"

//Main function, listens on TCP socket and tells a client hello
func main() {
    l, err := net.Listen("tcp", listenAddr)
    if err != nil {
        log.Fatal(err)
    }
    for {
        c, err := l.Accept()
        //Catch Errors
        if err != nil {
            log.Fatal(err)
        }
        //Tell the connected client Hello
        //TODO: This is a placeholder, remove it
        fmt.Fprintln(c, "Hello!")
        c.Close()
    }
}