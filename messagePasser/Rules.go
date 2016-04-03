////////////////////////////////////////////////////////////
//Multegula - Rules.go
//Rules.go defines the struct of rules and provides methods
//related to send and receive rules
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package messagePasser

import (
    "encoding/json"
    "fmt"
    "os"
)

/*
 * rule struct
 **/
type Rule struct {
    Action string // action of this rule
    Src string // the source of this rule
    Dest string // the destionation of this rule
    Kind string // the kind of message
    SeqNum int // the sequence number of message
}

/* this struct stores all send and receive rules */
type Rules struct {
    SendRules []Rule // send rules
    ReceiveRules []Rule // receive rules
}

/* stores all send and receive rules */
var rules Rules = Rules{}

/* init function, decode rules from rules.json */
func Init() {
    file, errOpenFile := os.Open("./rules.json")
    if errOpenFile != nil {
        fmt.Println("error when open file: ", errOpenFile)
    }
    decoder := json.NewDecoder(file)
    errDecode := decoder.Decode(&rules)
    if errDecode != nil {
        fmt.Println("error when decoding: ", errDecode)
    }
}

/**
 *find if there is a send rule which can be applied to message
 *@param  message
 *        message to be matched 
 *
 *@return if there is a send rule which can be applied to 
 *        message, return that send rule; otherwise, return 
 *        empty rule
 **/
func MatchSendRule(message Message) Rule {
    
}
