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
const CONSENSUS_CHANNEL_SIZE int = 10
const DELIMITER string = "::"

var leaderNode messagePasser.Node
var peerNodes messagePasser.Nodes
var localName string
var sendChannel chan *messagePasser.Message
var commitChannel chan *Proposal = make(chan *Proposal, CONSENSUS_CHANNEL_SIZE)
var acceptedProposals map[string]*Proposal
var isLeader bool

type Proposal struct {
	SeqNum int
	Type   string
	Value  string
}

func InitConsensus(leader messagePasser.Node, peers messagePasser.Nodes, localNodeName string) {
	localName = localNodeName
	leaderNode = leader
	peerNodes = peers
	acceptedProposals = make(map[string]*Proposal, CONSENSUS_CHANNEL_SIZE)
	sendChannel = make(chan *messagePasser.Message)
	isLeader = leader.Name == localNodeName
}

/*
 * If the leader, propose a value and reach consensus
 */
func Propose(proposal *Proposal) {
	//TODO
}

/*
 * Receives a consensus related message from the application's message dispatcher
 */
func ReceiveMessage(message messagePasser.Message) {
	proposal, err := contentToProposal(message.Content)
	if err != nil {
		fmt.Printf("Couldn't parse Consensus message:%+v\n", message)
		panic(err)
	}

	switch message.Kind {
	case CONSENSUS_PROPOSE_KIND:
		parseProposal(proposal)
	case CONSENSUS_COMMIT_KIND:
		commitProposal(proposal)
	default:
		handleProposalResponse(proposal)
	}
}

/*
 * Handles the response received from a peer in consensus process
 */
func handleProposalResponse(proposal *Proposal) {
	if !isLeader {
		return
	}
	//TODO
}

/*
 * Check with the application to see what value we agree to regarding the
 * proposal.Type
 */
func parseProposal(proposal *Proposal) {
	if isLeader {
		return
	}
	if accepted, exists := acceptedProposals[proposal.Type]; exists {
		// A proposal of the same type have already been accepted
		if accepted.Value == proposal.Value && accepted.SeqNum < proposal.SeqNum {
			accepted.SeqNum = proposal.SeqNum
			accept(proposal)
		} else {
			// proposal is not the most recent of that type so disregard
			reject(proposal)
		}
	} else {
		// It's a new proposal that hasn't been accepted
		localValue := check(proposal)
		if localValue == proposal.Value {
			acceptedProposals[proposal.Type] = proposal
			accept(proposal)
		} else {
			reject(proposal)
		}
	}
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

/*
 * Adds a proposal to commitProposal channel to be commited by application
 */
func commitProposal(proposal *Proposal) {
	// Make sure to remove the committed propsals
	delete(acceptedProposals, proposal.Type)
	commitChannel <- proposal
}

/*
 * Adds message to sendChannel to be retreived by the application and sent
 */
func addMessageToSendChannel(kind string, proposal *Proposal) {
	message := messagePasser.Message{
		Destination: leaderNode.Name,
		Source:      localName,
		Kind:        kind,
		Content:     proposalToContent(proposal)}
	sendChannel <- &message
}

/*
 * Returns the messages to be sent to the calling application
 */
func SendMessage() *messagePasser.Message {
	for {
		return <-sendChannel
	}
}

/*
 * Helper function to create Message.Content string from a Proposal
 */
func proposalToContent(proposal *Proposal) string {
	return fmt.Sprintf("%v%s%v%s%v", proposal.SeqNum, DELIMITER, proposal.Type, DELIMITER, proposal.Value)
}

/*
 * Helper function to create a Proposal from Message.Content string
 * The content will have the format "SeqNum::Type::Value"
 */
func contentToProposal(content string) (*Proposal, error) {
	values := strings.Split(content, DELIMITER)
	if len(values) != 3 {
		return nil, errors.New("Wrong Format: " + content)
	}
	seqNum, err := strconv.Atoi(values[0])
	if err != nil {
		return nil, err
	}
	return &Proposal{seqNum, values[1], values[2]}, nil
}
