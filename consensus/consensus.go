package consensus

import (
	"errors"
	"strings"

	"github.com/arminm/multegula/messagePasser"
)

const CONSENSUS_PROPOSE_KIND string = "CPK"
const CONSENSUS_ACCEPT_KIND string = "CAK"
const CONSENSUS_REJECT_KIND string = "CRK"
const CONSENSUS_COMMIT_KIND string = "CCK"

var leaderNode messagePasser.Node
var peerNodes messagePasser.Nodes

type Proposal struct {
	Type   string
	SeqNum string
	Value  string
}

var acceptedProposals = make(map[string]*Proposal)

func InitConsensus(leader messagePasser.Node, peers messagePasser.Nodes) {
	leaderNode = leader
	peerNodes = peers
}

func receiveMessage(message messagePasser.Message) {
	if message.Kind == CONSENSUS_PROPOSE_KIND {
		parseContent(message.Content) //type::num::val
	}
}

/*
 * Check with the application to see what value we agree to regarding the
 * proposal.Type
 */
func parseContent(content string) error {
	values := strings.Split(content, "::")
	if len(values) != 3 {
		return errors.New("Wrong Format!")
	}
	proposal := Proposal{values[0], values[1], values[2]}
	if accepted, exists := acceptedProposals[proposal.Type]; exists {
		if accepted.SeqNum < proposal.SeqNum {
			accepted.SeqNum = proposal.SeqNum
			accept(proposal)
		} else if accepted.SeqNum > proposal.SeqNum {
			reject(proposal)
		}
	} else {
		localValue := check(proposal)
		if localValue == proposal.Value {
			acceptedProposals[proposal.Type] = &proposal
			accept(proposal)
		} else {
			reject(proposal)
		}
	}

	return nil
}

/*
 * Check with the application to see what value we agree to regarding the
 * proposal.Type
 */
func check(proposal Proposal) string {
	return ""
}

/*
 * Accept the proposal
 */
func accept(proposal Proposal) {

}

/*
 * Reject the proposal
 */
func reject(proposal Proposal) {

}
