////////////////////////////////////////////////////////////
//Multegula - Defs.go
//This file defines all constants used in this project
//Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He
////////////////////////////////////////////////////////////

package defs

import (
	"time"
)

const HOLDBACKQUEUE_LIMIT int = 5

//Our bootstrap server.  Uncomment below for local testing.
// const SERVER_DNS string = "multegula.dyndns.org:55555"
const SERVER_DNS string = "localhost:55555"

/* The beginning of message types for bully algorithm */
/* These kinds of message will be used in bully algorithm */
/* The election message */
const MSG_BULLY_ELECTION string = "MUE"

/* The answer message */
const MSG_BULLY_ANSWER string = "MUA"

/* The unicorn message */
const MSG_BULLY_UNICORN string = "MUU"

/* Nodes request if unicorn is alive */
const MSG_BULLY_ARE_YOU_ALIVE string = "MUR"

/* The unicorn heart beat message */
const MSG_BULLY_IAM_ALIVE string = "MUL"

/* The end of message types for bully algorithm */

/* The default unicorn name */
/* Note that this name is reserved in the system */
const UNICORN_DEFAULT_NAME = "unicorn_default_name"

const DELIMITER string = "##"
const PAYLOAD_DELIMITER string = "|"

/* MessagePasser */
const QUEUE_SIZE int = 200

/* Bootstrap Server */
const MIN_PLAYERS_PER_GAME int = 2
const MAX_PLAYERS_PER_GAME int = 4
const TIMEOUT_DURATION = 10 * time.Second
const CHANNEL_SIZE = 10

/*** MESSAGE TYPE CONSTANTS ***/
const MSG_BALL_DEFLECTED string = "MBD"
const MSG_BALL_MISSED string = "MBM"
const MSG_BLOCK_BROKEN string = "MBB"
const MSG_CON_COMMIT string = "MCC"
const MSG_CON_CHECK string = "MCH"
const MSG_CON_REPLY string = "MCP"
const MSG_CON_REQ string = "MCR"
const MSG_DEAD_NODE string = "MDN"
const MSG_KILL_NODE string = "MKN"
const MSG_DEAD_UNICORN string = "MDU"
const MSG_GAME_TYPE string = "MGT"
const MSG_MYNAME string = "MMN"
const MSG_PADDLE_DIR string = "MPD"
const MSG_PAUSE_UPDATE string = "MPU"
const MSG_PLAYER_LOC string = "MPL"
const MSG_REJOIN_REQ string = "MRR"
const MSG_START_PLAY string = "MSP"
const MSG_SYNC_ERROR string = "MSE"
const MSG_UNICORN string = "MUN"


/*** MESSAGE DESTINATION CONSTANTS ***/
const MULTICAST_DEST string = "EVR1"
const MULTEGULA_DEST string = "MULT"
const UI_DEST string = "UI"

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

/*** IO REJOIN CONSTANTS ***/
const IO_REJOIN_DELAY_LIMIT int = 300
const IO_LASTGAME_NODES_FILENAME string = "lastgamenodes.mlg"
const IO_LASTGAME_TIME_FILENAME string = "lastgametime.mlg"
