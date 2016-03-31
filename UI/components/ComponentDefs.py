# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# ComponentDefs.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
from enum import Enum

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

### PowerUps - TODO : define powers ups here
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

### PlayerState - define different player states
class PlayerState(Enum) :
    USER        = 0 # controlled by this player
    AI          = 1 # controlling it self
    COMP        = 2 # controlled by a COMPetitor

### Tilt - defines the tilt of a block, either vertical or horizontal
class Tilt(Enum) :
    VERT    = 0
    HORZ    = 1
