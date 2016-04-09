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
    /* action of this rule
     * possible values are:
     * drop: drop message
     * dropAfter: drop message if SeqNum of message greater that SeqNum
     * delay: delay message until next send of message
     */
    Action string
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

/* the queue for delayed sending messages */
var sendDelayedQueue chan Message = make(chan Message, QUEUE_SIZE)

/* the queue for delayed receive messages */
var receiveDelayedQueue chan Message = make(chan Message, QUEUE_SIZE)


/* init function, decode rules from rules.json */
func initRules() {
    file, errOpenFile := os.Open("./messagePasser/rules.json")
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
 *if rule can be applied to message
 *@param message
 *       message to be tested
 *
 *@param rule
 *       rule to be applied
 *
 *@return if the rule can be applied to message,
 *        return true; otherwise return false
 */
func matchRule(message Message, rule Rule) bool {
    if len(rule.Src) > 0 && rule.Src != message.Source {
        return false
    }
    if len(rule.Dest) > 0 && rule.Dest != message.Destination {
        return false
    }
    if len(rule.Kind) > 0 && rule.Kind != message.Kind {
        return false
    }
    if rule.SeqNum > 0 {
        if rule.Action == "dropAfter" {
            if message.SeqNum <= rule.SeqNum {
                return false
            }
        } else {
            if message.SeqNum != rule.SeqNum {
                return false
            }
        }
    }
    return true
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
func matchSendRule(message Message) Rule {
    for _, rule := range rules.SendRules {
        if matchRule(message, rule) {
            return rule
        }
    }
    return Rule{}
}
/**
 *find if there is a receive rule which can be applied to message
 *@param  message
 *        message to be matched 
 *
 *@return if there is a receive rule which can be applied to 
 *        message, return that receive rule; otherwise, return 
 *        empty rule
 **/
func matchReceiveRule(message Message) Rule {
    for _, rule := range rules.ReceiveRules {
        if matchRule(message, rule) {
            return rule
        }
    }
    return Rule{}
}

/*
 *put message to sendDelayedQueue
 *@param message
 *       the message to be put into sendDelayedQueue
 **/
func putMessageToSendDelayedQueue(message Message) {
    sendDelayedQueue <- message
}

/*
 *put message to receiveDelayedQueue
 *@param message
 *       the message to be put into receiveDelayedQueue
 **/
func putMessageToReceiveDelayedQueue(message Message) {
    receiveDelayedQueue <- message
}
