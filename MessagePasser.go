////////////////////////////////////////////////////////////
//Multegula - MessagePasser.go 
//Multicasting Message Passer for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

import (
    "encoding/json"
    "os"
    "fmt"
)


//Config Reading Example
type Configuration struct {
    BootstrapServer    []string
}

file, _ := os.Open("config.json")
decoder := json.NewDecoder(file)
configuration := Configuration{}
err := decoder.Decode(&configuration)
if err != nil {
  fmt.Println("error:", err)
}
fmt.Println(configuration.BootstrapServer) // output: [BootstrapServer]
