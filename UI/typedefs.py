# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# typedefs.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
from enum import Enum

WALL_NAMES = ['warmin', 'waniel', 'warrett', 'wunwen']

### CONSTANT VALUES
# canvas dimensions
CANVAS_DIMENTSION = 350
CANVAS_WIDTH = CANVAS_DIMENTSION;
CANVAS_HEIGHT = CANVAS_DIMENTSION;
X_THIRD = CANVAS_WIDTH // 4
X_CENTER = CANVAS_WIDTH // 2
X_2THIRD = X_THIRD*3
Y_THIRD = CANVAS_HEIGHT // 4
Y_CENTER = CANVAS_HEIGHT // 2
Y_2THIRD = Y_THIRD*3
X_MARGIN = CANVAS_WIDTH // 30
Y_MARGIN = CANVAS_HEIGHT // 30
BORDER_WIDTH = CANVAS_WIDTH // 350

X_LIMIT_MIN = -(CANVAS_WIDTH // 2)
X_LIMIT_MAX = CANVAS_WIDTH*1.5
Y_LIMIT_MIN = -(CANVAS_HEIGHT // 2)
Y_LIMIT_MAX = CANVAS_HEIGHT*1.5

# text positions / sizing
Y_LOC_TITLE = CANVAS_HEIGHT // 4
Y_LOC_AUTHOR1 = CANVAS_HEIGHT*0.45
Y_LOC_AUTHOR2 = CANVAS_HEIGHT*0.50
Y_LOC_PROMPT = CANVAS_HEIGHT // 2
Y_LOC_GAME_OVER = CANVAS_HEIGHT*0.45
Y_LOC_WIN_TEASE = CANVAS_HEIGHT*0.6
Y_LOC_WINNER = CANVAS_HEIGHT*0.7
Y_LOC_TOP_BUTTON = 0.70*CANVAS_HEIGHT
Y_LOC_BOTTOM_BUTTON = 0.85*CANVAS_HEIGHT
S_TEXT_SIZE = CANVAS_WIDTH // 35
M_TEXT_SIZE = CANVAS_WIDTH // 28
L_TEXT_SIZE = CANVAS_WIDTH // 20
XL_TEXT_SIZE = CANVAS_WIDTH // 10

# button sizing / positions
BUTTON_X_SIZE = CANVAS_WIDTH // 8
BUTTON_Y_SIZE = CANVAS_HEIGHT // 18
BUTTON_MARGIN = (CANVAS_WIDTH // 10) - (CANVAS_WIDTH // 11)

# paddle sizing 
PADDLE_MARGIN = CANVAS_HEIGHT // 20
PADDLE_HEIGHT = CANVAS_HEIGHT // 50  
PADDLE_MIN = PADDLE_MARGIN + PADDLE_HEIGHT
PADDLE_MAX = CANVAS_WIDTH - PADDLE_MARGIN - PADDLE_HEIGHT
PADDLE_WIDTH_INIT = CANVAS_WIDTH // 6
PADDLE_WIDTH_MAX = (PADDLE_MAX - PADDLE_MIN) // 2

# block sizing
BLOCK_WIDTH = CANVAS_WIDTH // 10
BLOCK_HEIGHT = CANVAS_HEIGHT // 50  


# timing constants
DELAY = 30
REJOIN_TIMEOUT = 10000 // DELAY

# speed constants
BALL_SPEED_INIT = CANVAS_WIDTH // (120 - (DELAY*2))
PADDLE_SPEED_INIT = CANVAS_WIDTH // (120 - (DELAY*2))

# score int constants
LOST_LIFE_POINTS = -20
LOST_LIFE_LIVES = -1
EXTRA_LIFE_POINTS = 100
DEFLECT_POINTS  = 3
BREAK_POINTS = 5
INIT_LIVES = 10

# fixed point multiplier / rounding factor
FP_MULT = 10
RD_FACT = 1

# pause screen constants
DISP_3_VAL = 0
DISP_2_VAL = 50
DISP_1_VAL = 100
MOVE_ON_VAL = 150

# message formation and pervasion
BUFFER_SIZE = 200 #Arbitrary buffer size for received messages
DELIMITER = '##'
PAYLOAD_DELIMITER = '|'
LOCALHOST_IP = 'localhost'
DEFAULT_SRC = 'UNSET'
MULTICAST_DEST = 'EVR1'
MULTEGULA_DEST = 'MULT'
DEFAULT_PORT = 44444
PYMESSAGE_LEN = 4

### Orientation - for the location of players/paddles
class Orientation(Enum) :
    DIR_NORTH   = 0
    DIR_SOUTH   = 1
    DIR_EAST    = 2
    DIR_WEST    = 3

### Direction - movement directions
##  NOTE : currently only LEFT, RIGHT, and STOP are used for moving
##  the paddle.
class Direction(Enum) :
    DIR_STOP    = 0
    DIR_LEFT    = 1
    DIR_RIGHT   = 2
    DIR_UP      = 3
    DIR_DOWN    = 4

### PowerUps 
class PowerUps(Enum) :
    PWR_NONE            = 0 # no power up
    PWR_INC_PADDLE_W    = 1 # increase paddle width
    PWR_DEC_PADDLE_W    = 2 # decrease paddle width
    PWR_INC_PADDLE_S    = 3 # increase paddle speed
    PWR_DEC_PADDLE_S    = 4 # decrease paddle speed
    PWR_INC_BALL_R      = 4 # increase ball radius
    PWR_DEC_BALL_R      = 5 # decrease ball radius
    PWR_INC_BALL_V      = 6 # increase ball velocity
    PWR_DEC_BALL_V      = 7 # decrease ball velocity
    PWR_INC_LIFE        = 8 # add a life
    PWR_DEC_LIFE        = 9 # lose a live
    PWR_MOMENTUM        = 10 # ball momentum
    PWR_HOLD            = 11 # ball hold

### States - enumerate different states
class State(Enum) :
  STATES_NONE = 0
  STATE_SPLASH = 1
  STATE_MENU = 2
  STATE_PAUSE = 3
  STATE_GAMEPLAY = 4
  STATE_GAME_OVER = 5
  STATE_JOIN = 6
  STATE_REJOIN = 7
  STATE_SYNC = 8

### PlayerState - define different player states
class PlayerState(Enum) :
    USER        = 0 # controlled by this player
    AI          = 1 # controlling it self
    COMP        = 2 # controlled by a COMPetitor
    WALL        = 3 # player is a wall
    DEAD        = 4 # player is dead

### GameType - define the two game types
class GameType(Enum) :
    UNSET           = 0
    SINGLE_PLAYER   = 1
    MULTI_PLAYER    = 2

### Tilt - defines the tilt of a block, either vertical or horizontal
class Tilt(Enum) :
    VERT    = 0
    HORZ    = 1

### MsgType - defines the message types
class MsgType() :
    MSG_BALL_DEFLECTED  = 'MBD'
    MSG_BALL_MISSED     = 'MBM'
    MSG_BLOCK_BROKEN    = 'MBB'
    MSG_CON_CHECK       = 'MCH'
    MSG_CON_COMMIT      = 'MCC'
    MSG_CON_REPLY       = 'MCP'
    MSG_CON_REQ         = 'MCR'
    MSG_DEAD_NODE       = 'MDN'
    MSG_EXIT            = 'MEX'
    MSG_KILL_NODE       = 'MKN'
    MSG_GAME_TYPE       = 'MGT'
    MSG_MYNAME          = 'MMN'
    MSG_PADDLE_DIR      = 'MPD'
    MSG_PAUSE_UPDATE    = 'MPU'
    MSG_PLAYER_LOC      = 'MPL'
    MSG_REJOIN_REQ      = 'MRR'
    MSG_START_PLAY      = 'MSP'
    MSG_SYNC_ERROR      = 'MSE'
    MSG_UNICORN         = 'MUN'

### ConType - defines consensus types
class ConType() :
    CON_GAME_STATE = 'CGS'
    CON_REJOIN     = 'CRJ'

### MsgPayload - defines standard message payloads
class MsgPayload() :
    CON_REJOIN_YES      = 'Y'
    CON_REJOIN_NO       = 'N'
    GAME_TYPE_SINGLE    = 'S'
    GAME_TYPE_MULTI     = 'M'
    PADDLE_DIR_LEFT     = 'L'
    PADDLE_DIR_RIGHT    = 'R'
    PADDLE_DIR_STOP     = 'S'
    SYNC_ERR_BLOCK_BROKEN = 'BB'
    SYNC_ERR_BALL_DEFLECTED = 'BD'
    SYNC_ERR_CURRENT_STATE = 'CS'
    SYNC_ERR_DN_EXECUTE = 'DE'
    SYNC_ERR_EXECUTE = 'EX'
    SYNC_ERR_LAST_TO_TOUCH = 'LT'
    SYNC_ERR_NOT_UNICORN = 'NU'
    SYNC_ERR_PLAYER_LOC = 'PL'
    SYNC_ERR_PLAYER_TYPE = 'PT'


### MsgIndex - defines the the standard placement of payload values
class MsgIndex() :

    BALL_DEFLECTED_XCENTER  = 0
    BALL_DEFLECTED_YCENTER  = 1
    BALL_DEFLECTED_RADIUS   = 2
    BALL_DEFLECTED_XSPEED   = 3
    BALL_DEFLECTED_YSPEED   = 4
    BALL_DEFLECTED_SCORE    = 5
    BALL_MISSED_SCORE       = 0
    BALL_MISSED_LIVES       = 1
    BLOCK_BROKEN_XCENTER    = 0
    BLOCK_BROKEN_YCENTER    = 1
    BLOCK_BROKEN_RADIUS     = 2
    BLOCK_BROKEN_XSPEED     = 3
    BLOCK_BROKEN_YSPEED     = 4
    BLOCK_BROKEN_SCORE      = 5
    BLOCK_BROKEN_LIVES      = 6
    BLOCK_BROKEN_BLOCK      = 7
    CON_CHECK_TYPE          = 0
    CON_REJOIN_NODE         = 1
    CON_REJOIN_REPLY        = 2
    DEAD_NODE               = 0
    KILL_NODE               = 0
    PADDLE_DIR_DIR          = 0
    PADDLE_DIR_CENTER       = 1
    PADDLE_DIR_WIDTH        = 2
    PAUSE_UPDATE_VAL        = 0
    PAUSE_UPDATE_LEVEL      = 1
    PLAYER_LOC_NUMBER       = 0
    PLAYER_LOC_PLAYERS      = 1
    REJOIN_REQ_NODE         = 0
    START_PLAY_XSPEED       = 0
    START_PLAY_YSPEED       = 1
    UNICORN_UNICORN         = 0

class PlayerReturnStatus() :
    NO_STATUS       = 0
    WALL_NO_STATUS  = 1
    DEAD_NO_STATUS  = 2
    BALL_MISSED     = 3
    BALL_DEFLECTED  = 4
    WALL_BALL_DEFLECTED = 5
    DEAD_BALL_DEFLECTED = 6
    BLOCK_BROKEN    = 7
    BALL_OOB        = 8

class PauseReturnStatus() :
    NO_STATUS   = 0
    DISP_3      = 1
    DISP_2      = 2
    DISP_1      = 3
    MOVE_ON     = 4

class LevelReturnStatus() :
    NO_STATUS   = 0
    COMPLETE    = 1
    GAME_OVER   = 2

# PyMessage class 
class PyMessage :
    ### __init__ - initialize and return an empty PyMessage
    def __init__(self):
        self.kind = ''
        self.src = ''
        self.dest = ''
        self.seqNum = -1
        self.content = None
        self.multicast = False

    ### crack - crack a PyMessage from the the 'received' string
    def crack(self, received):
        receivedArray = str(received).split(DELIMITER)
        try :
            self.src = receivedArray[0]
            self.dest = receivedArray[1]
            self.seqNum = receivedArray[2]
            self.content = receivedArray[3].split(PAYLOAD_DELIMITER)
            self.kind = receivedArray[4]
        except :
            print('CANNOT CRACK: ' + received)

    ### assemble - assemble the message and return
    def assemble(self):
        return self.src + DELIMITER + self.dest + DELIMITER + self.content + DELIMITER + self.kind + '\n'

    ### toString - return a visually appealing string relective of the contents in the message
    def toString(self):
        return 'source: ' + self.src + ', type: ' + self.kind + ', content: ' + str(self.content)

ARTIFICIAL_COMMIT_1 = "CGS|4|armin|23|3|daniel|53|5|lunwen|10|1|garrett|19|4|0|101110111101110111010"
ARTIFICIAL_COMMIT_2 = "CGS|4|armin|23|3|daniel|53|5|lunwen|10|1|garrett|19|4|2|1101101111011011101101100011"
ARTIFICIAL_COMMIT_3 = "CGS|3|armin|23|3|daniel|53|5|lunwen|10|1|1|101101101101101101011"




