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
    elif payload == MsgPayload.PADDLE_DIR_STOP :
        direction = Direction.DIR_STOP
        return direction

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
        if state in [PlayerState.USER, PlayerState.COMP, PlayerState.AI] and lives > 0 :
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

### sendSyncError - formulate and send sync error
def sendKillMessage(content, canvas) :
    # form message
    toSend = PyMessage()
    toSend.src = canvas.data['myName']
    toSend.kind = MsgType.MSG_KILL_NODE
    toSend.content = content
    toSend.multicast = True
    print("SENDING: " + toSend.toString())
    # send message
    sendMessage(toSend, canvas)

### sendMessage - use dictionary flags in the 'myReceived' entry to avoid sending 
##      duplicate messages and avoid synchronization issues. (e.g. breaking the same block twice)
def sendMessage(message, canvas) :
    if canvas.data['myReceived'][message.kind] == True and canvas.data['artificialDead'] != True : 
        canvas.data['bridge'].sendMessage(message)
        canvas.data['myReceived'][message.kind] = False
    elif canvas.data['artificialDead'] == True :
        print("LOOK WE DEAD -> " + message.toString())
    else : 
        print(canvas.data['myName'] + " UI DROPPING MSG: " + message.toString())

### getGameState - stringify the game state for sending in consensus requests
def getGameState(canvas) :    
    # get alphabetical player names
    playerList = []
    for player in canvas.data['competitors'] :
        if canvas.data[player].state in [PlayerState.USER, PlayerState.COMP] :
            playerList.append(player)    
    numPlayers = str(len(playerList))
    playerList = sorted(playerList)

    # intialize content
    content = numPlayers

    # add player information to the message
    for player in playerList :
        content += '|'
        name = canvas.data[player].name
        score = str(canvas.data[player].score)
        lives = str(canvas.data[player].lives)
        center = str(canvas.data[player].paddle.center)
        width = str(canvas.data[player].paddle.width)
        content += (name + '|' + score + '|' + lives + '|' + center + '|' + width)

    # add level information to the message
    content += ('|' + str(canvas.data['level'].currentLevel))

    # add block information to the message
    for i, block in enumerate(canvas.data['level'].blocks) :
        if block.enabled == True :
            content += ('|' + str(i))

    # finish and return message  
    return content

### reactToCommit - set appropriate data values based on received messages
def reactToCommit(content, canvas) :
    print(canvas.data['myName'] + " COMMITING : " + str(content))
    conType = content[MsgIndex.CON_CHECK_TYPE]

    if conType == ConType.CON_GAME_STATE :
        i = MsgIndex.CON_CHECK_TYPE

        i += 1
        numPlayers = int(content[i]) # number of players
        aliveList = []

        ## update player stats
        for j in range(0, numPlayers) :
            i += 1
            player = content[i] # name
            aliveList.append(player)
            canvas.data[player].first = True
            canvas.data[player].paddle.first = True
            i += 1
            canvas.data[player].score = int(content[i]) # score
            i += 1
            canvas.data[player].lives = int(content[i]) # lives
            i += 1
            canvas.data[player].paddle.center = int(content[i]) # center
            i += 1
            canvas.data[player].paddle.width = int(content[i]) # width

        ## kill players
        for player in canvas.data['competitors'] :
            if player not in aliveList and player in canvas.data:
                canvas.data[player].iAmDead()

        ## set the level
        i += 1
        level = int(content[i]) # level
        canvas.data['level'].currentLevel = level
        canvas.data['level'].blocks = canvas.data['level'].levels[level]
        canvas.data['level'].first = True
        canvas.data['level'].updated = True
        canvas.data['gameScreen'].first = True

        ## update the blocks
        i += 1
        # loop through all blocks 
        for b, block in enumerate(canvas.data['level'].blocks) :
            # disable any blocks that are appropriate to do so
            if str(b) not in content[i:]:
                canvas.data['level'].blocks[b].enabled = False
                canvas.data['level'].blocks[b].first = False
            else :
                canvas.data['level'].blocks[b].enabled = True
                canvas.data['level'].blocks[b].first = True

        canvas.data['ball'].reset()
        canvas.data['currentState'] = State.STATE_PAUSE
        canvas.data['artificalSync'] = False

    elif conType == ConType.CON_REJOIN :
        # get the node in question and the reply
        missingNode = content[MsgIndex.CON_REJOIN_NODE]
        reply = content[MsgIndex.CON_REJOIN_REPLY]
        
        # remove missing node from the list
        if missingNode in canvas.data['missingNodes'] :
            canvas.data['missingNodes'].remove(missingNode)

        # kill node if appropriate
        if reply == MsgPayload.CON_REJOIN_NO :
            canvas.data[missingNode].iAmDead()

        # reset flags
        canvas.data['artificialDead'] = False
        canvas.data['attemptingRejoin'] = False
        clearMyReceivedFlags(canvas)

        # if there are still missing nodes, go back to the rejoin state. Otherwise, sync up!
        if canvas.data['missingNodes'] :
            canvas.data['currentState'] = State.STATE_REJOIN
        else :
            canvas.data['currentState'] = State.STATE_SYNC


### clearMyReceivedFlags - so the game can persist in a graceful manner
def clearMyReceivedFlags(canvas) :
    canvas.data['myReceived'][MsgType.MSG_BALL_DEFLECTED] = True
    canvas.data['myReceived'][MsgType.MSG_BALL_MISSED] = True
    canvas.data['myReceived'][MsgType.MSG_BLOCK_BROKEN] = True
    canvas.data['myReceived'][MsgType.MSG_DEAD_NODE] = True
    canvas.data['myReceived'][MsgType.MSG_KILL_NODE] = True
    canvas.data['myReceived'][MsgType.MSG_CON_CHECK] = True
    canvas.data['myReceived'][MsgType.MSG_CON_COMMIT] = True
    canvas.data['myReceived'][MsgType.MSG_CON_REQ] = True
    canvas.data['myReceived'][MsgType.MSG_CON_REPLY] = True
    canvas.data['myReceived'][MsgType.MSG_GAME_TYPE] = True
    canvas.data['myReceived'][MsgType.MSG_MYNAME] = True
    canvas.data['myReceived'][MsgType.MSG_PADDLE_DIR] = True
    canvas.data['myReceived'][MsgType.MSG_PAUSE_UPDATE] = True
    canvas.data['myReceived'][MsgType.MSG_PLAYER_LOC] = True
    canvas.data['myReceived'][MsgType.MSG_START_PLAY] = True
    canvas.data['myReceived'][MsgType.MSG_SYNC_ERROR] = True
    canvas.data['myReceived'][MsgType.MSG_UNICORN] = True

### resetGamePlay - reset the screen for play
def resetGamePlay(canvas) :
    # reset the level
    canvas.data['level'].first = True
    canvas.data['level'].updated = True
    for b, block in enumerate(canvas.data['level'].blocks) :
        if canvas.data['level'].blocks[b].enabled == True :
            canvas.data['level'].blocks[b].first = True

    # reset the game screen
    canvas.data['gameScreen'].first = True

    # reset the players
    for player in canvas.data['competitors'] :
        if canvas.data[player].state in [PlayerState.USER, PlayerState.COMP]:
            canvas.data[player].first = True
            canvas.data[player].paddle.first = True

    # reset ball and go to pause state
    canvas.data['ball'].reset()