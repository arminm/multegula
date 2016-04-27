package consensus

import (
	"errors"
	"fmt"
	"strconv"
	"strings"
	"time"

	"github.com/arminm/multegula/defs"
	"github.com/arminm/multegula/messagePasser"
)

var leaderNode messagePasser.Node
var peerNodes messagePasser.Nodes
var localName string
var isLeader bool
var commitChannel chan *Proposal = make(chan *Proposal, defs.CONSENSUS_CHANNEL_SIZE)
var sendChannel chan *messagePasser.Message

// A proposal check channel that passes check jobs to be completed by application
var proposalCheckChannel chan *PropCheck = make(chan *PropCheck, defs.CONSENSUS_CHANNEL_SIZE)

// Client
var acceptedProposals map[string]*Proposal

// Leader
var SeqNum int = 0
var propVotesMap map[string]*(map[string]*Proposal)

type Proposal struct {
	SeqNum int
	Type   string
	Value  string
}

type PropCheck struct {
	Prop     *Proposal
	Callback *func(string)
}

func InitConsensus(leader messagePasser.Node, peers messagePasser.Nodes, localNodeName string) {
	localName = localNodeName
	leaderNode = leader
	peerNodes = peers
	isLeader = leader.Name == localNodeName
	sendChannel = make(chan *messagePasser.Message, defs.CONSENSUS_CHANNEL_SIZE)

	//Client
	acceptedProposals = make(map[string]*Proposal)

	//Leader
	propVotesMap = make(map[string]*(map[string]*Proposal))

}

/*
 * If the leader, propose a value and reach consensus
 */
func Propose(value string, valueType string) {
	if !isLeader {
		return
	}
	// Create proposal
	SeqNum += 1
	proposal := Proposal{SeqNum, valueType, value}
	// Create the votesMap to track votes
	votesMap := make(map[string]*Proposal)
	// Add own proposal to votesMap
	votesMap[localName] = &proposal
	// Keep track of the votesMap for the valueType
	propVotesMap[valueType] = &votesMap
	// Multicast the proposal
	addMessageToSendChannel(defs.MULTICAST_DEST, defs.CONSENSUS_PROPOSE_KIND, &proposal)
	// local copy of SeqNum for timeout checks
	seqNum := SeqNum
	time.AfterFunc(defs.CONSENSUS_TIMEOUT_INTERVAL, func() {
		// check if the timeout is still relevant
		if votes, exists := propVotesMap[valueType]; exists {
			localVote := (*Proposal)((*votes)[localName])
			if localVote.SeqNum == seqNum {
				// Timed out, see if consensus is reached
				reached, value, err := reachedConsensus(valueType)
				if err == nil {
					if reached {
						// update localVote's value to decided value and multicastCommit
						proposal.Value = value
						multicastCommit(&proposal)
					} else {
						// If timed out and haven't reached consensus then force value
						multicastCommit(&proposal)
					}
				}
			}
		}
	})
}

/*
 * Multicasts a commit asking everyone to commit value
 */
func multicastCommit(proposal *Proposal) {
	// Check to see if we haven't already multicasted a commit for this proposal
	if votes, exists := propVotesMap[proposal.Type]; exists {
		if (*votes)[localName].SeqNum == proposal.SeqNum {
			delete(propVotesMap, proposal.Type)
			addMessageToSendChannel(defs.MULTICAST_DEST, defs.CONSENSUS_COMMIT_KIND, proposal)
			// locally commit as well.
			commitChannel <- proposal
		}
	}
}

/*
 * Receives a consensus related message from the application's message dispatcher
 */
func ReceiveMessage(message messagePasser.Message) {
	proposal, err := stringToProposal(message.Content)
	if err != nil {
		fmt.Printf("Couldn't parse Consensus message:%+v\n", message)
		panic(err)
	}

	switch message.Kind {
	case defs.CONSENSUS_PROPOSE_KIND:
		parseProposal(proposal)
	case defs.CONSENSUS_COMMIT_KIND:
		commitProposal(proposal)
	default:
		// Message is for the leader
		handleProposalResponse(&message, proposal)
	}
}

/*
 * Handles the response received from a peer in consensus process
 */
func handleProposalResponse(message *messagePasser.Message, proposal *Proposal) {
	if !isLeader {
		return
	}
	votesMapPtr, exists := propVotesMap[proposal.Type]
	if !exists {
		return
	}
	localVote := (*Proposal)((*votesMapPtr)[localName])
	if localVote.SeqNum != proposal.SeqNum {
		return
	}
	(*votesMapPtr)[message.Source] = proposal
	if len(*votesMapPtr) == len(peerNodes)+1 {
		reached, value, err := reachedConsensus(proposal.Type)
		if err != nil {
			return
		}
		if reached {
			consensus := localVote
			consensus.Value = value
			multicastCommit(consensus)
		} else {
			multicastCommit(localVote)
		}
	}
}

/*
 * Looks at the existing votes to see if majority consensus has been reached
 */
func reachedConsensus(valueType string) (bool, string, error) {
	votes, exists := propVotesMap[valueType]
	if !exists {
		return false, "N/A", errors.New("ValueType not found in propVotesMap")
	}

	// Find majority vote
	var popularVote string
	popularCount := 0
	for _, vote := range *votes {
		tempCount := 0
		for _, compareVote := range *votes {
			if vote.Value == compareVote.Value {
				tempCount += 1
			}
		}
		if tempCount > popularCount {
			popularCount = tempCount
			popularVote = vote.Value
		}
	}
	if popularCount <= len(peerNodes)/2 {
		return false, "N/A", nil
	}

	return true, popularVote, nil
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
			proposal.Value = accepted.Value
			reject(proposal)
		}
	} else {
		// It's a new proposal that hasn't been accepted
		callback := func(value string) {
			if value == proposal.Value {
				acceptedProposals[proposal.Type] = proposal
				accept(proposal)
			} else {
				proposal.Value = value
				reject(proposal)
			}
		}
		check(proposal, &callback)
	}
}

/*
 * Check with the application to see what value we agree to regarding the
 * proposal.Type
 */
func check(proposal *Proposal, callback *func(string)) {
	propCheck := PropCheck{proposal, callback}
	proposalCheckChannel <- &propCheck
}

/*
 * Returns outstanding proposal checks to be done.
 */
func ProposalCheck() *PropCheck {
	return <-proposalCheckChannel
}

/*
 * Accept the proposal
 */
func accept(proposal *Proposal) {
	addMessageToSendChannel(leaderNode.Name, defs.CONSENSUS_ACCEPT_KIND, proposal)
}

/*
 * Reject the proposal
 */
func reject(proposal *Proposal) {
	addMessageToSendChannel(leaderNode.Name, defs.CONSENSUS_REJECT_KIND, proposal)
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
 * return proposals that should be committed
 */
func ProposalToCommit() *Proposal {
	return <-commitChannel
}

/*
 * Adds message to sendChannel to be retreived by the application and sent
 */
func addMessageToSendChannel(dest string, kind string, proposal *Proposal) {
	message := messagePasser.Message{
		Destination: dest,
		Source:      localName,
		Kind:        kind,
		Content:     proposalToString(proposal)}
	sendChannel <- &message
}

/*
 * Returns the messages to be sent to the calling application
 */
func SendMessage() *messagePasser.Message {
	return <-sendChannel
}

/*
 * Helper function to create Message.Content string from a Proposal
 */
func proposalToString(proposal *Proposal) string {
	return fmt.Sprintf("%v%s%v%s%v", proposal.SeqNum, defs.CONSENSUS_DELIMITER, proposal.Type, defs.CONSENSUS_DELIMITER, proposal.Value)
}

/*
 * Helper function to create a Proposal from Message.Content string
 * The content will have the format "SeqNum::Type::Value"
 */
func stringToProposal(content string) (*Proposal, error) {
	values := strings.Split(content, defs.CONSENSUS_DELIMITER)
	if len(values) != 3 {
		return nil, errors.New("Wrong Format: " + content)
	}
	seqNum, err := strconv.Atoi(values[0])
	if err != nil {
		return nil, err
	}
	return &Proposal{seqNum, values[1], values[2]}, nil
}
