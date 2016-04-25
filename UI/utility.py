# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# utility.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
from UI.components.control.Level import *
from UI.components.control.Player import *
from UI.components.gameplay.Ball import *
from UI.components.gameplay.Block import *
from UI.components.gameplay.Paddle import *
from UI.components.directive.Button import *
from UI.components.directive.TextField import *
from UI.components.screens.GameOverScreen import *
from UI.components.screens.GameScreen import *
from UI.components.screens.JoinScreen import *
from UI.components.screens.MenuScreen import *
from UI.components.screens.PauseScreen import *
from UI.components.screens.SplashScreen import *
from UI.components.screens.SyncScreen import *
from UI.typedefs import *

### translateBallSpeed - translate speed based on orientation
def translateBallSpeed(xSpeed, ySpeed, player) :
    orientation = player.ORIENTATION

    # if there is a wall, then do not translate
    if orientation == Orientation.DIR_SOUTH :
        return (xSpeed, ySpeed)
    elif orientation == Orientation.DIR_EAST : 
        return (ySpeed, -xSpeed)
    elif orientation == Orientation.DIR_NORTH :
        return (-xSpeed, -ySpeed)
    elif orientation == Orientation.DIR_WEST :
        return (-ySpeed, xSpeed)

### translateBallPosition - translate position based on orientation
def translateBallPosition(xCenter, yCenter, radius, player) :
    orientation = player.ORIENTATION
    if orientation == Orientation.DIR_SOUTH :
        return (xCenter, yCenter)
    elif orientation == Orientation.DIR_EAST :
        return (yCenter, CANVAS_HEIGHT - xCenter)
    elif orientation == Orientation.DIR_NORTH :
        return (CANVAS_WIDTH - xCenter, CANVAS_HEIGHT - yCenter)
    elif orientation == Orientation.DIR_WEST :
        return (CANVAS_WIDTH - yCenter, xCenter)

### translatePlayerDirection - translate player direction based on orientation
def translatePlayerDirection(payload, player) :
    orientation = player.ORIENTATION

    # translate from payload type to Direction type
    if payload == MsgPayload.PADDLE_DIR_LEFT :
        direction = Direction.DIR_LEFT
    elif payload == MsgPayload.PADDLE_DIR_RIGHT :
        direction = Direction.DIR_RIGHT 

    # translate based on orientation
    if orientation == Orientation.DIR_SOUTH :
        return direction
    elif orientation == Orientation.DIR_EAST  and direction == Direction.DIR_LEFT :
        return Direction.DIR_RIGHT
    elif orientation == Orientation.DIR_EAST and direction == Direction.DIR_RIGHT :
        return Direction.DIR_LEFT
    elif orientation == Orientation.DIR_NORTH and direction == Direction.DIR_LEFT :
        return Direction.DIR_RIGHT
    elif orientation == Orientation.DIR_NORTH and direction == Direction.DIR_RIGHT :
        return Direction.DIR_LEFT
    elif orientation == Orientation.DIR_WEST :
        return direction

### translatePlayerLocation - translate player location based on orientation
def translatePlayerLocaiton(center, player) :
    orientation = player.ORIENTATION

    if orientation == Orientation.DIR_SOUTH :
        return center
    elif orientation == Orientation.DIR_EAST :
        return CANVAS_HEIGHT - center
    elif orientation == Orientation.DIR_NORTH :
        return CANVAS_WIDTH - center
    elif orientation == Orientation.DIR_WEST :
        return center

### getWinner - determin who the winner is
def getWinner(canvas) :
    winner = 'THE DEVELOPERS!'
    winningScore = 0

        # update all players
    for player in canvas.data['competitors'] :
        (name, state, score, lives, pwr) = canvas.data[player].getStatus()
        if (state == PlayerState.USER or state == PlayerState.COMP) and lives > 0 :
            score = score + lives*EXTRA_LIFE_POINTS
            if score > winningScore :
                winner = name
                winningScore = score

    return (winner, winningScore)

### isGameOver - determine if the game has been completed
def isGameOver(canvas) :
    alive_count = 0
    # update all players
    for player in canvas.data['competitors'] :
        (name, state, score, lives, pwr) = canvas.data[player].getStatus()
        if (state == PlayerState.USER or state == PlayerState.COMP) and lives > 0 :
            alive_count += 1
    if alive_count == 1 :
        return True
    return False

### sendSyncError - formulate and send sync error
def sendSyncError(content, canvas) :
    # form message
    toSend = PyMessage()
    toSend.src = canvas.data['myName']
    toSend.kind = MsgType.MSG_SYNC_ERROR
    toSend.content = content
    toSend.multicast = True

    print("SENDING: " + toSend.toString())

    # send message
    canvas.data['bridge'].sendMessage(toSend)