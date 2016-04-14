////////////////////////////////////////////////////////////
//Multegula - MessageType.go
//Multicasting Message Passer for Multegula
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////
// This file defines all message types used in this project
////////////////////////////////////////////////////////////

package messageType

/* 
 * The size of queues
 */
const QUEUE_SIZE int = 100

/* The beginning of message types for bully algorithm */
/* These kinds of message will be used in bully algorithm */
/* The election message */
const ELECTION string = "ELECTION"
/* The answer message */
const ANSWER string = "ANSWER"
/* The unicorn message */	
const UNICORN string = "UNICORN"
/* Nodes request if unicorn is alive */
const ARE_YOU_ALIVE string = "ARE_YOU_ALIVE"
/* The unicorn heart beat message */
const IAM_ALIVE string = "IAM_ALIVE"
/* The end of message types for bully algorithm */

const MSG_PADDLE_POS string = "MSG_PADDLE_POS"
const MSG_PADDLE_DIR string = "MSG_PADDLE_DIR"

const UI_MULTICAST_DEST string = "EVERYBODY"
const UI_MULTEGULA_DEST string = "MULTEGULA"
const MSG_MYNAME string = "MSG_MYNAME"

const UI_SOURCE string = "UI"
