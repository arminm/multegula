package consensus

import (
	"errors"
	"fmt"
	"strconv"
	"strings"

	"github.com/arminm/multegula/messagePasser"
)

const CONSENSUS_PROPOSE_KIND string = "CPK"
const CONSENSUS_ACCEPT_KIND string = "CAK"
const CONSENSUS_REJECT_KIND string = "CRK"
const CONSENSUS_COMMIT_KIND string = "CCK"
const DELIMITER string = "::"

var leaderNode messagePasser.Node
var peerNodes messagePasser.Nodes
var localName string
var sendChannel chan *messagePasser.Message

type Proposal struct {
	SeqNum int
	Type   string
	Value  string
}

var acceptedProposals map[string]*Proposal

func InitConsensus(leader messagePasser.Node, peers messagePasser.Nodes, localNodeName string) {
	localName = localNodeName
	leaderNode = leader
	peerNodes = peers
	acceptedProposals = make(map[string]*Proposal)
	sendChannel = make(chan *messagePasser.Message)
}

func ReceiveMessage(message messagePasser.Message) {
	if message.Kind == CONSENSUS_PROPOSE_KIND {
		parseProposal(message.Content) //SeqNum::type::val
	}
}

/*
 * Check with the application to see what value we agree to regarding the
 * proposal.Type
 */
func parseProposal(content string) error {
	values := strings.Split(content, DELIMITER)
	if len(values) != 3 {
		return errors.New("Wrong Format: " + content)
	}
	seqNum, err := strconv.Atoi(values[0])
	if err != nil {
		return err
	}
	proposal := Proposal{seqNum, values[1], values[2]}
	if accepted, exists := acceptedProposals[proposal.Type]; exists {
		if accepted.Value == proposal.Value && accepted.SeqNum < proposal.SeqNum {
			accepted.SeqNum = proposal.SeqNum
			accept(&proposal)
		} else {
			reject(&proposal)
		}
	} else {
		localValue := check(&proposal)
		if localValue == proposal.Value {
			acceptedProposals[proposal.Type] = &proposal
			accept(&proposal)
		} else {
			reject(&proposal)
		}
	}

	return nil
}

/*
 * Check with the application to see what value we agree to regarding the
 * proposal.Type
 */
func check(proposal *Proposal) string {
	return ""
}

/*
 * Accept the proposal
 */
func accept(proposal *Proposal) {
	addMessageToSendChannel(CONSENSUS_ACCEPT_KIND, proposal)
}

/*
 * Reject the proposal
 */
func reject(proposal *Proposal) {
	addMessageToSendChannel(CONSENSUS_REJECT_KIND, proposal)
}

func addMessageToSendChannel(kind string, proposal *Proposal) {
	message := messagePasser.Message{
		Destination: leaderNode.Name,
		Source:      localName,
		Kind:        kind,
		Content:     proposalToContent(proposal)}
	sendChannel <- &message
}

func SendMessage() *messagePasser.Message {
	for {
		return <-sendChannel
	}
}

func proposalToContent(proposal *Proposal) string {
	return fmt.Sprintf("%v%s%v%s%v", proposal.SeqNum, DELIMITER, proposal.Type, DELIMITER, proposal.Value)
}
