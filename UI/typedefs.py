# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# ComponentDefs.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
from enum import Enum

### CONSTANT VALUES
# canvas dimensions
CANVAS_WIDTH = 700;
CANVAS_HEIGHT = 700;
X_THIRD = CANVAS_WIDTH // 4
X_CENTER = CANVAS_WIDTH // 2
X_2THIRD = X_THIRD*3
Y_THIRD = CANVAS_HEIGHT // 4
Y_CENTER = CANVAS_HEIGHT // 2
Y_2THIRD = Y_THIRD*3
X_MARGIN = CANVAS_WIDTH // 30
Y_MARGIN = CANVAS_HEIGHT // 30
BORDER_WIDTH = CANVAS_WIDTH // 350

# text positions / sizing
Y_LOC_TITLE = CANVAS_HEIGHT // 4
Y_LOC_AUTHOR1 = CANVAS_HEIGHT*0.45
Y_LOC_AUTHOR2 = CANVAS_HEIGHT*0.50
Y_LOC_PROMPT = CANVAS_HEIGHT // 2
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

# speed constants
BALL_SPEED_INIT = CANVAS_WIDTH // 110
PADDLE_SPEED_INIT = CANVAS_WIDTH // 80

# score int constants
LOST_LIFE_POINTS = -20
LOST_LIFE_LIVES = -1
DEFLECT_POINTS  = 3
BREAK_POINTS = 5

# fixed point multiplier / rounding factor
FP_MULT = 100
RD_FACT = 2

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

### Screens - enumerate different screens
class Screens(Enum) :
  SCRN_NONE = 0
  SCRN_SPLASH = 1
  SCRN_MENU = 2
  SCRN_PAUSE = 3
  SCRN_GAME = 4
  SCRN_GAME_OVER = 5

### PlayerState - define different player states
class PlayerState(Enum) :
    USER        = 0 # controlled by this player
    AI          = 1 # controlling it self
    COMP        = 2 # controlled by a COMPetitor
    WALL        = 3 # player is a wall

### GameType - define the two game types
class GameType(Enum) :
    SINGLE_PLAYER   = 0
    MULTI_PLAYER    = 1

### Tilt - defines the tilt of a block, either vertical or horizontal
class Tilt(Enum) :
    VERT    = 0
    HORZ    = 1

### MsgType - defines the message types
class MsgType() :
    MSG_GAME_TYPE   = 'MGT'
    MSG_MYNAME      = 'MMN'
    MSG_PADDLE_DIR  = 'MPD'
    MSG_PADDLE_POS  = 'MPP'
    MSG_BALL_MISSED = 'MBM'
    MSG_BALL_DEFLECTED = 'MBD'
    MSG_BLOCK_BROKEN = 'MBB'

### MsgPayload - defines standard message payloads
class MsgPayload() :
    GAME_TYPE_SINGLE    = 'S'
    GAME_TYPE_MULTI     = 'M'
    PADDLE_DIR_LEFT     = 'L'
    PADDLE_DIR_RIGHT    = 'R'

### MsgIndex - defines the the standard placement of payload values
class MsgIndex() :
    PADDLE_DIR              = 0
    PADDLE_POS_CENTER       = 0
    PADDLE_POS_WIDTH        = 1
    BALL_MISSED_SCORE       = 0
    BALL_MISSED_LIVES       = 1
    BALL_DEFLECTED_XCENTER  = 0
    BALL_DEFLECTED_YCENTER  = 1
    BALL_DEFLECTED_RADIUS   = 2
    BALL_DEFLECTED_XSPEED   = 3
    BALL_DEFLECTED_YSPEED   = 4
    BALL_DEFLECTED_SCORE    = 5
    BLOCK_BROKEN_XCENTER    = 0
    BLOCK_BROKEN_YCENTER    = 1
    BLOCK_BROKEN_RADIUS     = 2
    BLOCK_BROKEN_XSPEED     = 3
    BLOCK_BROKEN_YSPEED     = 4
    BLOCK_BROKEN_SCORE      = 5
    BLOCK_BROKEN_LIVES      = 6
    BLOCK_BROKEN_BLOCK      = 7

class PlayerReturnStatus() :
    NO_STATUS       = 0
    WALL_NO_STATUS  = 1
    BALL_MISSED     = 2
    BALL_DEFLECTED  = 3
    WALL_BALL_DEFLECTED = 4
    BLOCK_BROKEN    = 5




