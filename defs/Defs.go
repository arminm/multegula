////////////////////////////////////////////////////////////
//Multegula - Defs.go
//This file defines all constants used in this project
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package defs

import (
	"time"
)

//Our bootstrap server.  Uncomment below for local testing.
//const SERVER_DNS string = "multegula.dyndns.org:55555"
const SERVER_DNS string = "localhost:55555"

/* The beginning of message types for bully algorithm */
/* These kinds of message will be used in bully algorithm */
/* The election message */
const ELECTION string = "election"

/* The answer message */
const ANSWER string = "answer"

/* The coordinator message */
const COORDINATOR string = "coordinator"

/* The end of message types for bully algorithm */
const DELIMITER string = "##"
const PAYLOAD_DELIMITER string = "|"

/* MessagePasser */
const QUEUE_SIZE int = 200

/* Bootstrap Server */
const MIN_PLAYERS_PER_GAME int = 2
const MAX_PLAYERS_PER_GAME int = 4
const TIMEOUT_DURATION = 30 * time.Second
const CHANNEL_SIZE = 10

/*** MESSAGE TYPE CONSTANTS ***/
const MSG_GAME_TYPE string = "MGT"
const MSG_MYNAME string = "MMN"
const MSG_PADDLE_POS string = "MPP"
const MSG_PADDLE_DIR string = "MPD"
const MSG_BALL_MISSED string = "MBM"
const MSG_BALL_DEFLECTED string = "MBD"
const MSG_BLOCK_BROKEN string = "MBB"
const MSG_PLAYER_LOC string = "MPL"

/*** MESSAGE DESTINATION CONSTANTS ***/
const MULTICAST_DEST string = "EVR1"
const MULTEGULA_DEST string = "MULT"

/*** MESSAGE SOURCE CONTENTS ***/
const UI_SOURCE string = "UI"

/*** MESSAGE PAYLOAD CONSTANTS ***/
const GAME_TYPE_MULTI string = "M"
const GAME_TYPE_SINGLE string = "S"

const DEFAULT_GAME_PORT int = 11111
const DEFAULT_UI_PORT int = 44444

/*** CONSENSUS CONSTANTS ***/
const CONSENSUS_PROPOSE_KIND string = "CPK"
const CONSENSUS_ACCEPT_KIND string = "CAK"
const CONSENSUS_REJECT_KIND string = "CRK"
const CONSENSUS_COMMIT_KIND string = "CCK"
const CONSENSUS_CHANNEL_SIZE int = 10
const CONSENSUS_TIMEOUT_INTERVAL time.Duration = 5 * time.Second
const CONSENSUS_DELIMITER string = "::"
