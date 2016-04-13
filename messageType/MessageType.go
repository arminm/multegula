////////////////////////////////////////////////////////////
//Multegula - MessageType.go
//Multicasting Message Passer for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////
// This file defines all message types used in this project
////////////////////////////////////////////////////////////

package messageType

type MessageType int

const (
	/* The beginning of message types for bully algorithm */
	/* These kinds of message will be used in bully algorithm */
	/* The election message */
	ELECTION MessageType = 1 + iota
	/* The answer message */
	ANSWER
	/* The coordinator message */	
	COORDINATOR
	/* The end of message types for bully algorithm */
)

var messageTypes = [...]string{
	/* The beginning of message type values for bully algorithm */
	"election"
	"answer"
	"coordinator"
	/* The end of message type values for bully algorithm */
}

func (messageType MessageType) String() string {
	return messageTypes[messageType - 1]
}