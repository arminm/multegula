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
const SERVER_DNS string = "multegula.dyndns.org:55555"
//const SERVER_DNS string = "localhost:55555"

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

const DELIMITER string = "##"

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
