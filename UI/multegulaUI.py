# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# multegulaUI.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
from tkinter import *
import random
#Lets us look back a directory for functions
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

# import stuff from our package
import threading
from bridges.GoBridge import *
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
from UI.components.screens.RejoinScreen import *
from UI.components.screens.SplashScreen import *
from UI.components.screens.SyncScreen import *
from UI.components import *
from UI.typedefs import *
from UI.utility import *

### keyPressed - handle keypressed events
def keyPressed(event) :
    canvas = event.widget.canvas
    currentState = canvas.data['currentState']
    gameType = canvas.data['gameType']
    myName  = canvas.data['myName']

    ### ARTIFICIAL SYNC ENGINE ###
    ## start a natural game state sync
    if event.char == '!' and gameType == GameType.MULTI_PLAYER and currentState == State.STATE_GAMEPLAY :
        content = MsgPayload.SYNC_ERR_EXECUTE + '|' + canvas.data['myName']
        sendSyncError(content, canvas)

    ## start a manual game state sync - to be followed by the next two commands '#', '$', and '%' 
    elif event.char == '@' and gameType == GameType.MULTI_PLAYER and currentState == State.STATE_GAMEPLAY :
        content = MsgPayload.SYNC_ERR_DN_EXECUTE + '|' + canvas.data['myName']
        sendSyncError(content, canvas)

    ## manual game sync #1
    elif event.char == '1' and currentState == State.STATE_SYNC and canvas.data['artificalSync'] == True :
        toSend = PyMessage()
        toSend.src = myName
        toSend.kind = MsgType.MSG_CON_COMMIT
        toSend.content = ARTIFICIAL_COMMIT_1
        toSend.multicast = True
        # send message
        canvas.data['bridge'].sendMessage(toSend)

    ## manual game sync #2
    elif event.char == '2' and currentState == State.STATE_SYNC and canvas.data['artificalSync'] == True :
        toSend = PyMessage()
        toSend.src = myName
        toSend.kind = MsgType.MSG_CON_COMMIT
        toSend.content = ARTIFICIAL_COMMIT_2
        toSend.multicast = True
        # send message
        canvas.data['bridge'].sendMessage(toSend)

    ## manual game sync #3
    elif event.char == '3' and currentState == State.STATE_SYNC and canvas.data['artificalSync'] == True :
        toSend = PyMessage()
        toSend.src = myName
        toSend.kind = MsgType.MSG_CON_COMMIT
        toSend.content = ARTIFICIAL_COMMIT_3
        toSend.multicast = True
        # send message
        canvas.data['bridge'].sendMessage(toSend)

    ### ARTIFICIAL REJOIN ENGINE ###
    # lost the node
    elif event.char == '#' and gameType == GameType.MULTI_PLAYER :
        toSend = PyMessage()
        toSend.src = myName
        toSend.kind = MsgType.MSG_DEAD_NODE
        toSend.content = myName
        toSend.multicast = True
        # send message
        canvas.data['bridge'].sendMessage(toSend)
        canvas.data['artificialDead'] = True

    # attempt rejoin
    elif event.char == '1' and gameType == GameType.MULTI_PLAYER and canvas.data['artificialDead'] == True :
        toSend = PyMessage()
        toSend.src = myName
        toSend.kind = MsgType.MSG_REJOIN_REQ
        toSend.content = myName
        toSend.multicast = True
        canvas.data['bridge'].sendMessage(toSend)

    # handle splash screen events - entering a name
    elif currentState == State.STATE_SPLASH :
        # add new characters
        if 'A' <= event.char <= 'Z' or 'a' <= event.char <= 'z' :
            canvas.data['splashTextField'].addChar(event.char)            
        # remove characters
        elif event.keysym == 'BackSpace' :
            canvas.data['splashTextField'].deleteChar()            
        # addd space 
        elif event.keysym == 'space' :
            canvas.data['splashTextField'].addChar(' ')            
        # enter the name
        elif (event.keysym == 'Return') and canvas.data['splashTextField'].changed :
            canvas.data['currentState'] = State.STATE_MENU
            # set name
            myName = canvas.data['splashTextField'].text

            # replace spaces and make sure there are no duplicates with WALL_NAMES
            myName = myName.replace(' ', '')
            if myName in WALL_NAMES :
                myName += '1'
            elif myName in [LOCALHOST_IP, DEFAULT_SRC, MULTICAST_DEST, MULTEGULA_DEST] :
                myName += '1'
            elif not myName :
                myName += '1'

            canvas.data['myName'] = myName

            # send name up to Multegula!
            toSend = PyMessage()
            toSend.src = myName
            toSend.kind = MsgType.MSG_MYNAME
            toSend.content = myName
            toSend.multicast = False
            sendMessage(toSend, canvas)

    # pause screen / gameplay keyPressed events - move the paddle
    elif currentState in [State.STATE_PAUSE, State.STATE_GAMEPLAY] :
        myPaddle = canvas.data[myName].paddle

        ### MOVE PADDLE LEFT ###
        # if (event.keysym == 'Left') or (event.keysym == 'a') or (event.keysym == 'A') :
        if event.keysym in ['Left', 'a', 'A'] :
            # if this is a multi-player game, the direction is not already set, and the paddle can move,
            #   then it is okay to send an update
            if canvas.data['gameType'] == GameType.MULTI_PLAYER :
                if myPaddle.direction != Direction.DIR_LEFT and myPaddle.canMove(Direction.DIR_LEFT) :
                    # get message content
                    CENTER = canvas.data[myName].paddle.center
                    WIDTH = canvas.data[myName].paddle.width

                    # create and send message
                    toSend = PyMessage()
                    toSend.src =  myName
                    toSend.kind = MsgType.MSG_PADDLE_DIR
                    toSend.content = MsgPayload.PADDLE_DIR_LEFT + '|' + str(CENTER) + '|' + str(WIDTH)
                    toSend.multicast = True
                    sendMessage(toSend, canvas)
                    canvas.data[canvas.data['myName']].paddle.direction = Direction.DIR_STOP

            # if this is a single player game, then go ahead and set the paddle direction
            elif canvas.data['gameType'] == GameType.SINGLE_PLAYER : 
                canvas.data[canvas.data['myName']].paddle.direction = Direction.DIR_LEFT

        ### MOVE PADDLE RIGHT ####
        elif event.keysym in ['Right', 'd', 'D'] :
            # if this is a multi-player game, the direction is not already set, and the paddle can move,
            #   then it is okay to send an update.  
            if canvas.data['gameType'] == GameType.MULTI_PLAYER : 
                if myPaddle.direction != Direction.DIR_RIGHT and myPaddle.canMove(Direction.DIR_RIGHT):
                    # get message content
                    CENTER = canvas.data[myName].paddle.center
                    WIDTH = canvas.data[myName].paddle.width

                    # create and send message
                    toSend = PyMessage()
                    toSend.src = myName
                    toSend.kind = MsgType.MSG_PADDLE_DIR
                    toSend.content = MsgPayload.PADDLE_DIR_RIGHT + '|' + str(CENTER) + '|' + str(WIDTH)
                    toSend.multicast = True
                    sendMessage(toSend, canvas)
                    canvas.data[canvas.data['myName']].paddle.direction = Direction.DIR_STOP

            # if this is a single player game, then go ahead and set the paddle direction
            elif canvas.data['gameType'] == GameType.SINGLE_PLAYER : 
                canvas.data[canvas.data['myName']].paddle.direction = Direction.DIR_RIGHT

    ### STOP PADDLE MOTION ###
    if currentState in [State.STATE_PAUSE, State.STATE_GAMEPLAY] :
        if event.keysym in ['space', 's', 'S', 'Down'] :
            # if this is a multi-player game, the direction is not already set then it is okay to send and update
            if canvas.data['gameType'] == GameType.MULTI_PLAYER: 
                if canvas.data[canvas.data['myName']].paddle.direction != Direction.DIR_STOP:
                    myName = canvas.data['myName']
                    # get message content
                    CENTER = canvas.data[myName].paddle.center
                    WIDTH = canvas.data[myName].paddle.width

                    #create and send message                    
                    toSend = PyMessage()
                    toSend.src = myName
                    toSend.kind = MsgType.MSG_PADDLE_DIR
                    toSend.content = MsgPayload.PADDLE_DIR_STOP + '|' + str(CENTER) + '|' + str(WIDTH)
                    toSend.multicast = True
                    sendMessage(toSend, canvas)
                    canvas.data[canvas.data['myName']].paddle.direction = Direction.DIR_STOP

            # if this is a single player game, then go ahead and set the paddle direction
            elif canvas.data['gameType'] == GameType.SINGLE_PLAYER: 
                canvas.data[canvas.data['myName']].paddle.direction = Direction.DIR_STOP

### mousePressed - handle mouse press events
def mousePressed(event) :
    canvas = event.widget.canvas
    # main screen mouse pressed events - button clicks
    if canvas.data['currentState'] == State.STATE_MENU : 
        # check solo button pressed
        if canvas.data['soloButton'].clicked(event.x, event.y) :
            # initialize players
            canvas.data['gameType'] = GameType.SINGLE_PLAYER
            initPlayers(canvas)

            # send message to Multegula
            toSend = PyMessage()
            toSend.src = canvas.data['myName']
            toSend.kind = MsgType.MSG_GAME_TYPE
            toSend.content = MsgPayload.GAME_TYPE_SINGLE
            toSend.multicast = False
            sendMessage(toSend, canvas)

            # initialize game
            canvas.data['currentState'] = State.STATE_PAUSE

            # initialize ball
            canvas.data['ball'].reset()
            canvas.delete(ALL)
        # check joine button pressed
        elif canvas.data['joinButton'].clicked(event.x, event.y) :
            # initialize players
            canvas.data['gameType'] = GameType.MULTI_PLAYER

            # send message to multegula
            toSend = PyMessage()
            toSend.src = canvas.data['myName']
            toSend.kind = MsgType.MSG_GAME_TYPE
            toSend.content = MsgPayload.GAME_TYPE_MULTI
            toSend.multicast = False
            sendMessage(toSend, canvas)

            # initialize game
            canvas.data['currentState'] = State.STATE_JOIN
            canvas.delete(ALL)

### react - react to messages
def react(canvas, received) :
    # break down message
    kind = received.kind
    name = received.src
    content = received.content
    myName = canvas.data['myName']
    currentState = canvas.data['currentState']

    # reset teh myReceived blag
    if name == myName :
        canvas.data['myReceived'][kind] = True

    # MSG_BALL_DEFLECTED - deflect a ball
    if kind == MsgType.MSG_BALL_DEFLECTED :
        # get sending players state
        playerState = canvas.data[name].state

        # only USERs and COMPs should be sending network messages
        if playerState in [PlayerState.USER, PlayerState.COMP] :
            # this should only happen in the GAMEPLAY state
            if currentState == State.STATE_GAMEPLAY : 
                # get information out of payload
                score   = int(content[MsgIndex.BALL_DEFLECTED_SCORE])
                xCenter = float(content[MsgIndex.BALL_DEFLECTED_XCENTER]) / FP_MULT
                yCenter = float(content[MsgIndex.BALL_DEFLECTED_YCENTER]) / FP_MULT
                xSpeed  = float(content[MsgIndex.BALL_DEFLECTED_XSPEED]) / FP_MULT
                ySpeed  = float(content[MsgIndex.BALL_DEFLECTED_YSPEED]) / FP_MULT
                radius  = float(content[MsgIndex.BALL_DEFLECTED_RADIUS]) / FP_MULT

                # translate for player orientation
                (xSpeed, ySpeed) = translateBallSpeed(xSpeed, ySpeed, canvas.data[name])
                (xCenter, yCenter) = translateBallPosition(xCenter, yCenter, radius, canvas.data[name])

                # set component fields
                canvas.data[name].score = score
                canvas.data[name].statusUpdate = True
                canvas.data['ball'].lastToTouch = name
                canvas.data['ball'].setCenter(xCenter, yCenter)
                canvas.data['ball'].radius = radius
                canvas.data['ball'].setVelocity(xSpeed, ySpeed)
                canvas.data['ball'].randomColor()
            # otherwise, we are out of sync!!
            elif currentState != State.STATE_SYNC :
                content = MsgPayload.SYNC_ERR_CURRENT_STATE + '|' + str(currentState) + '|' + MsgType.MSG_BALL_DEFLECTED + '|' + name
                sendSyncError(content, canvas)
        # otherwise, we are out of sync!
        elif currentState != State.STATE_SYNC :
            content = MsgPayload.SYNC_ERR_PLAYER_TYPE + '|' + MsgType.MSG_BALL_DEFLECTED + '|' + name
            sendSyncError(content, canvas)

    # MSG_BALL_MISSED - miss the ball
    elif kind == MsgType.MSG_BALL_MISSED : 
        # get sending players state
        playerState = canvas.data[name].state

        # only USERs and COMPs should be sending network messages
        if playerState in [PlayerState.USER, PlayerState.COMP] :
            # this should only happen in the GAMEPLAY state
            if currentState == State.STATE_GAMEPLAY :
                # get information out of payload 
                score = int(content[MsgIndex.BALL_MISSED_SCORE])
                lives = int(content[MsgIndex.BALL_MISSED_LIVES])

                # set component fields
                canvas.data[name].score = score
                canvas.data[name].lives = lives
                canvas.data[name].statusUpdate = True
                canvas.data['ball'].reset()

                if isGameOver(canvas) == True :
                    canvas.delete(ALL)
                    canvas.data['winner'] = getWinner(canvas);
                    canvas.data['currentState'] = State.STATE_GAME_OVER
                else :
                    canvas.data['currentState'] = State.STATE_PAUSE
            # otherwise, we are out of sync!
            elif currentState != State.STATE_SYNC :
                content = MsgPayload.SYNC_ERR_CURRENT_STATE + '|' + str(currentState) + '|' + MsgType.MSG_BALL_MISSED + '|' + name
                sendSyncError(content, canvas)
        # otherwise, we are out of sync!
        elif currentState != State.STATE_SYNC :
            content = MsgPayload.SYNC_ERR_PLAYER_TYPE + '|' + MsgType.MSG_BALL_MISSED + '|' + name
            sendSyncError(content, canvas)

    # MSG_BLOCK_BROKEN - break a block
    elif kind == MsgType.MSG_BLOCK_BROKEN :
        # get sending players state
        playerState = canvas.data[name].state

        # only USERs and COMPs should be sending network messages
        if playerState in [PlayerState.USER, PlayerState.COMP] :
            # this should only happen in the GAMEPLAY state
            if currentState == State.STATE_GAMEPLAY :
                # the sender has to be the last person to touch the ball
                if canvas.data['ball'].lastToTouch == name :
                    # get information out of payload
                    score   = int(content[MsgIndex.BLOCK_BROKEN_SCORE])
                    lives   = int(content[MsgIndex.BLOCK_BROKEN_LIVES])
                    xCenter = float(content[MsgIndex.BLOCK_BROKEN_XCENTER]) / FP_MULT
                    yCenter = float(content[MsgIndex.BLOCK_BROKEN_YCENTER]) / FP_MULT
                    xSpeed  = float(content[MsgIndex.BLOCK_BROKEN_XSPEED]) / FP_MULT
                    ySpeed  = float(content[MsgIndex.BLOCK_BROKEN_YSPEED]) / FP_MULT
                    radius  = float(content[MsgIndex.BLOCK_BROKEN_RADIUS]) / FP_MULT
                    block   = int(content[MsgIndex.BLOCK_BROKEN_BLOCK])

                    # only an ENABLED block can be broken
                    if canvas.data['level'].blocks[block].enabled == True :     
                        # translate for player orientation
                        (xSpeed, ySpeed) = translateBallSpeed(xSpeed, ySpeed, canvas.data[name])
                        (xCenter, yCenter) = translateBallPosition(xCenter, yCenter, radius, canvas.data[name])

                        # set component fields
                        canvas.data[name].score = score
                        canvas.data[name].lives = lives
                        canvas.data[name].statusUpdate = True
                        canvas.data['ball'].lastToTouch = name
                        canvas.data['ball'].setCenter(xCenter, yCenter)
                        canvas.data['ball'].radius = radius
                        canvas.data['ball'].setVelocity(xSpeed, ySpeed)
                        canvas.data['ball'].randomColor()
                        canvas.data['level'].blocks[int(content[MsgIndex.BLOCK_BROKEN_BLOCK])].disable()
                        canvas.data['level'].updated = True
                    # otherwise we are out of sync !
                    elif currentState != State.STATE_SYNC :
                        content = MsgPayload.SYNC_ERR_BLOCK_BROKEN + '|' + str(block) + '|' + name
                        sendSyncError(content, canvas)
                # otherwse we are out of sync !
                elif currentState != State.STATE_SYNC :
                    content = MsgPayload.SYNC_ERR_LAST_TO_TOUCH + '|' + name
                    sendSyncError(content, canvas)
            # otherwse we are out of sync !
            elif currentState != State.STATE_SYNC :
                content = MsgPayload.SYNC_ERR_CURRENT_STATE + '|' + str(currentState) + '|' + MsgType.MSG_BLOCK_BROKEN + '|' + name
                sendSyncError(content, canvas)
        # otherwise, we are out of sync!
        elif currentState != State.STATE_SYNC :
            content = MsgPayload.SYNC_ERR_PLAYER_TYPE + '|' + MsgType.MSG_BLOCK_BROKEN + '|' + name
            sendSyncError(content, canvas)

    # MSG_CON_COMMIT - commit a consensus result
    elif kind == MsgType.MSG_CON_COMMIT :
        canvas.delete(ALL)
        reactToCommit(content, canvas)
        print("Multegula has been syncronized!")

    # MSG_FORCE_COMMIT - force a commit
    elif kind == MsgType.MSG_FORCE_COMMIT :
        canvas.delete(ALL)
        reactToCommit(content, canvas)
        print("Multegula has been syncronized!")

    # MSG_CON_CHECK - respond to a concensus check
    elif kind == MsgType.MSG_CON_CHECK :
        # con only receive this message while SYNCING or REJOINING 
        if currentState in [State.STATE_SYNC, State.STATE_REJOIN] :
            # get the type of consensus 
            conType = content[MsgIndex.CON_CHECK_TYPE]

            # if this is game state concensus, respond appropriates
            if conType == ConType.CON_GAME_STATE :
                response = ConType.CON_GAME_STATE + '|' + getGameState(canvas)

            # rejoin consensus, respond appropriately
            elif conType == ConType.CON_REJOIN :
                requestingNode = content[MsgIndex.CON_REJOIN_NODE]
                if requestingNode in canvas.data['missingNodes'] :
                    response = ConType.CON_REJOIN + '|' + requestingNode + '|' + MsgPayload.CON_REJOIN_YES
                else :
                    response = ConType.CON_REJOIN + '|' + requestingNode + '|' + MsgPayload.CON_REJOIN_NO

            # respond
            toSend = PyMessage()
            toSend.src = myName
            toSend.kind = MsgType.MSG_CON_REPLY
            toSend.content = response
            toSend.multicast = False
            sendMessage(toSend, canvas)
        # otherwise, we are out of sync!
        else :
            content = MsgPayload.SYNC_ERR_CURRENT_STATE + '|' + str(currentState) + '|' + MsgType.MSG_BLOCK_BROKEN + '|' + name
            sendSyncError(content, canvas)           

    # MSG_DEAD_NODE - a dead node has been detected
    elif kind == MsgType.MSG_DEAD_NODE :
        missingNode = content[MsgIndex.DEAD_NODE]

        # this message can happen at any time
        if currentState != State.STATE_REJOIN :
            canvas.delete(ALL)
            canvas.data['gameScreen'].first = True
            canvas.data['level'].updated = True
            canvas.data['ball'].reset()
            canvas.data['currentState'] = State.STATE_REJOIN

        # get the dead node, add it to the list, make a timer

        if missingNode not in canvas.data['missingNodes'] :
            canvas.data['missingNodes'].append(missingNode)
            canvas.data[missingNode + 'Timer'] = REJOIN_TIMEOUT


    # MSG_KILL_NODE - this missing node's timeout has expired
    elif kind == MsgType.MSG_KILL_NODE :
        missingNode = content[MsgIndex.KILL_NODE]
        canvas.data[missingNode].iAmDead()
        if missingNode in canvas.data['missingNodes'] :
            canvas.data['missingNodes'].remove(missingNode)
            print("We cannot wait for " + missingNode + " any longer...moving on.")

    # MSG_PADDLE_DIR - move a paddle
    elif kind == MsgType.MSG_PADDLE_DIR :
        # get sending players state
        playerState = canvas.data[name].state

        # only USERs and COMPs should be sending network messages
        if playerState in [PlayerState.USER, PlayerState.COMP] :
            # only can move paddles in the PAUSE and GAMEPLAY states
            if currentState in [State.STATE_PAUSE, State.STATE_GAMEPLAY] :
                # get information out of payload
                direction = content[MsgIndex.PADDLE_DIR_DIR]
                center = int(content[MsgIndex.PADDLE_DIR_CENTER])
                width = int(content[MsgIndex.PADDLE_DIR_WIDTH])

                # translate for player orientation
                direction = translatePlayerDirection(direction, canvas.data[name])
                center = translatePlayerLocaiton(center, canvas.data[name])

                # set component fields
                canvas.data[name].paddle.direction = direction
                canvas.data[name].paddle.center = center
                canvas.data[name].paddle.width = width

            # otherwise you are out of sync!!
            elif currentState != State.STATE_SYNC :
                content = MsgPayload.SYNC_ERR_CURRENT_STATE + '|' + str(currentState) + '|' + MsgType.MSG_PADDLE_DIR + '|' + name
                sendSyncError(content, canvas)
        # otherwise you are out of sync!!
        elif currentState != State.STATE_SYNC :
            content = MsgPayload.SYNC_ERR_PLAYER_TYPE + '|' + MsgType.MSG_PADDLE_DIR + '|' + name
            sendSyncError(content, canvas)

    # MSG_PAUSE_UPDATE - update the pause screen
    elif kind == MsgType.MSG_PAUSE_UPDATE :
        # should only get this in the PAUSE state
        if currentState == State.STATE_PAUSE :
            unicorn = canvas.data['unicorn']
            # only the unicorn sends these messages
            if name == unicorn:
                canvas.data['pauseScreen'].text = content[MsgIndex.PAUSE_UPDATE_VAL]
                canvas.data['ball'].reset()

            # otherwise we are out of sync!
            elif currentState != State.STATE_SYNC :
                content = MsgPayload.SYNC_ERR_NOT_UNICORN + '|' + MsgType.MSG_PAUSE_UPDATE + '|' + name
                sendSyncError(content, canvas)
        # otherwise you are out of sync!!
        elif currentState != State.STATE_SYNC :
            content = MsgPayload.SYNC_ERR_CURRENT_STATE + '|' + str(currentState) + '|' + MsgType.MSG_PAUSE_UPDATE + '|' + name
            sendSyncError(content, canvas)

    # MSG_PLAYER_LOC - player location on startup
    elif kind == MsgType.MSG_PLAYER_LOC :
        # if the players have not been initialized, then go ahead and do that
        if canvas.data['playersInitialized'] == False: 
            initPlayers(canvas, int(content[MsgIndex.PLAYER_LOC_NUMBER]), content[MsgIndex.PLAYER_LOC_PLAYERS:])
            canvas.data['ball'].reset()
            canvas.data['currentState'] = State.STATE_PAUSE

        # if the players have been initialized, then check to make sure the received message matches
        #   exactly what was received previously
        else :
            # get all players out of the competitor list (walls also appear in the competitors list)
            playerList = []
            for player in canvas.data['competitors'] :
                if state in [PlayerState.USER, PlayerState.COMP] :
                    playerList.append(player)

            receivedList = content[MsgIndex.PLAYER_LOC_PLAYERS]

            if playerList != receivedList and currentState != State.STATE_SYNC :
                content = MsgPayload.SYNC_ERR_PLAYER_LOC + '|' + name
                sendSyncError(content, canvas)

    # MSG_REJOIN_REQ  - try and rejoin the network
    elif kind == MsgType.MSG_REJOIN_REQ :
        # get the missing node
        missingNode = content[MsgIndex.REJOIN_REQ_NODE]
        print(missingNode + " has requested to rejoin the game.")

        if missingNode in canvas.data['missingNodes'] and canvas.data['unicorn'] == myName :
            # form message
            toSend = PyMessage()
            toSend.src = myName
            toSend.kind = MsgType.MSG_REJOIN_ACK
            toSend.content = missingNode
            toSend.multicast = True 
            # send message
            sendMessage(toSend, canvas)
            print("\tThe more the merrier. C'mon back " + missingNode + ".")

        elif canvas.data['unicorn'] == myName :
            print("\tThe game has moved on. " + missingNode + "cannot rejoin.")

        # reset the timer
        timerKey = missingNode + 'Timer'
        canvas.data[timerKey] = REJOIN_TIMEOUT

    elif kind == MsgType.MSG_REJOIN_ACK :
        missingNode = content[MsgIndex.REJOIN_ACK_NODE]
        if missingNode in canvas.data['missingNodes'] :
            canvas.data['missingNodes'].remove(missingNode)

    # MSG_START_PLAY
    elif kind == MsgType.MSG_START_PLAY :
        # should only get this in the PAUSE state
        if currentState == State.STATE_PAUSE :
            unicorn = canvas.data['unicorn']

            if name == unicorn :
                # pull information from the payload
                xSpeed = float(content[MsgIndex.START_PLAY_XSPEED]) / FP_MULT
                ySpeed = float(content[MsgIndex.START_PLAY_YSPEED]) / FP_MULT

                # translate for player orientation
                (xSpeed, ySpeed) = translateBallSpeed(xSpeed, ySpeed, canvas.data[name])

                # update the player's paddle
                canvas.data['ball'].setVelocity(xSpeed, ySpeed)
                canvas.data['pauseScreen'].reset(canvas)
                canvas.data['currentState'] = State.STATE_GAMEPLAY

            # ontherswise, we are stupid swamped
            elif currentState != State.STATE_SYNC :
                content = MsgPayload.SYNC_ERR_NOT_UNICORN + '|' + MsgType.MSG_START_PLAY + '|' + name
                sendSyncError(content, canvas)
        # otherwise you are out of sync!!
        elif currentState != State.STATE_SYNC :
            content = MsgPayload.SYNC_ERR_CURRENT_STATE + '|' + str(currentState) + '|' + MsgType.MSG_START_PLAY + '|' + name
            sendSyncError(content, canvas)

    # MSG_SYNC_ERROR - syncronization error has occurrect
    elif kind == MsgType.MSG_SYNC_ERROR :
        # go to the sync error state
        if currentState not in [State.STATE_SYNC, State.STATE_REJOIN] :
            canvas.delete(ALL)
            canvas.data['gameScreen'].first = True
            canvas.data['level'].updated = True
            canvas.data['ball'].reset()
            canvas.data['currentState'] = State.STATE_SYNC

            if content[MsgIndex.CON_CHECK_TYPE] == MsgPayload.SYNC_ERR_DN_EXECUTE :
                canvas.data['artificalSync'] = True

    # MSG_UNICORN
    elif kind == MsgType.MSG_UNICORN :
        canvas.data['unicorn'] = content[MsgIndex.UNICORN_UNICORN]
        print('UI now riding on ' + canvas.data['unicorn'] + '.')

### receiveAll - get all messages from the GoBrige
def receiveAll(canvas) :
    # loop until there are no
    while True:
        message = canvas.data['bridge'].receiveMessage();
        if message.src == '':
            break
        else:
            react(canvas, message)

### playerUpdate - react to player update
##  RETURN TRUE if the player is still playing, False otherwise
def playerUpdate(name, status, info, canvas) :
    # single player game -> directly update appropriate game information
    if canvas.data['gameType'] == GameType.SINGLE_PLAYER :
        # BALL_MISSED -> update status and reset, player is alive -> return True 
        if status == PlayerReturnStatus.BALL_MISSED :
            canvas.data[name].score += LOST_LIFE_POINTS
            canvas.data[name].lives += LOST_LIFE_LIVES
            canvas.data[name].statusUpdate = True

            if isGameOver(canvas) == True :
                canvas.delete(ALL)
                canvas.data['winner'] = getWinner(canvas);
                canvas.data['currentState'] = State.STATE_GAME_OVER
            else :
                canvas.data['ball'].reset()
                canvas.data['currentState'] = State.STATE_PAUSE

        # BALL_DEFLECTED -> update status and set ball properties, player is alive -> Return True
        elif status == PlayerReturnStatus.BALL_DEFLECTED :
            canvas.data[name].score += DEFLECT_POINTS
            canvas.data[name].statusUpdate = True
            canvas.data['ball'].lastToTouch = name;    
            canvas.data['ball'].setVelocity(info[0], info[1])  
            canvas.data['ball'].randomColor()
        
        # BLOCK_BROKEN -> update status, set ball properties, update level, player is alive -> Return True
        elif status == PlayerReturnStatus.BLOCK_BROKEN :
            canvas.data[name].score += BREAK_POINTS;    
            canvas.data[name].statusUpdate = True
            canvas.data['ball'].setVelocity(info[0], info[1])  
            canvas.data['level'].blocks[info[2]].disable()
            canvas.data['level'].updated = True

        # DEAD_BALL_DEFLECTED -> update ball properties, player is dead -> Return False
        elif status == PlayerReturnStatus.DEAD_BALL_DEFLECTED :
            canvas.data['ball'].setVelocity(info[0], info[1])  
            canvas.data['ball'].randomColor()

    # multiplayer game -> send update to competitors
    elif canvas.data['gameType'] == GameType.MULTI_PLAYER :
        # BALL_MISSED -> created MSG_BALL_MISSED, player is alive -> return True 
        if status == PlayerReturnStatus.BALL_MISSED :
            # get message content fields
            SCORE = canvas.data[name].score + LOST_LIFE_POINTS
            LIVES = canvas.data[name].lives + LOST_LIFE_LIVES

            # form message
            toSend = PyMessage()
            toSend.src = name
            toSend.kind = MsgType.MSG_BALL_MISSED
            toSend.content = str(SCORE) + '|' + str(LIVES)
            toSend.multicast = True 
            # send message
            sendMessage(toSend, canvas)

        # BALL_DEFLECTED -> create MSG_BALL_DEFLECTED, player is alive -> Return True
        elif status == PlayerReturnStatus.BALL_DEFLECTED :
            ball  = canvas.data['ball']
            # get message content fields
            RADIUS = round(ball.radius * FP_MULT)
            XSPEED = round(info[0] * FP_MULT)
            YSPEED = round(info[1] * FP_MULT)
            XCENTER = round((ball.xCenter + info[0]) * FP_MULT)
            YCENTER = round((ball.yCenter + info[1]) * FP_MULT)
            SCORE = canvas.data[name].score + DEFLECT_POINTS

            # form message
            toSend = PyMessage()
            toSend.src = name
            toSend.kind = MsgType.MSG_BALL_DEFLECTED
            toSend.content = (str(XCENTER) + '|' + str(YCENTER) + '|' + 
                                str(RADIUS) + '|' + str(XSPEED) + '|' + 
                                str(YSPEED) + '|' + str(SCORE))
            toSend.multicast = True
            # send message
            sendMessage(toSend, canvas)
            canvas.data['ball'].setVelocity(0, 0)


        # WALL_BALL_DEFLECTED -> update ball properties, not a player -> Return False
        elif status == PlayerReturnStatus.WALL_BALL_DEFLECTED :
            canvas.data['ball'].setVelocity(info[0], info[1])  
            canvas.data['ball'].randomColor()

        # DEAD_BALL_DEFLECTED -> update ball properties, player is dead -> Return False
        elif status == PlayerReturnStatus.DEAD_BALL_DEFLECTED :
            canvas.data['ball'].setVelocity(info[0], info[1])  
            canvas.data['ball'].randomColor()

        # BLOCK_BROKEN -> create MSG_BLOCK_BROKEN, player is alive -> Return True
        elif status == PlayerReturnStatus.BLOCK_BROKEN :
            ball  = canvas.data['ball']
            # get message content fields
            RADIUS = round(ball.radius * FP_MULT)
            XSPEED = round(info[0] * FP_MULT)
            YSPEED = round(info[1] * FP_MULT)
            XCENTER = round((ball.xCenter + info[0]) * FP_MULT)
            YCENTER = round((ball.yCenter + info[1]) * FP_MULT)
            SCORE = canvas.data[name].score + BREAK_POINTS
            LIVES = canvas.data[name].lives #TODO: update with power up
            BLOCK = info[2]

            # form message
            toSend = PyMessage()
            toSend.src = name
            toSend.kind = MsgType.MSG_BLOCK_BROKEN
            toSend.content = (str(XCENTER) + '|' + str(YCENTER) + '|' + 
                                str(RADIUS) + '|' + str(XSPEED) + '|' + 
                                str(YSPEED) + '|' + str(SCORE) + '|' +
                                str(LIVES) + '|' + str(BLOCK))
            toSend.multicast = True
            # send message
            sendMessage(toSend, canvas)
            canvas.data['ball'].setVelocity(0, 0)

        # BALL_OOB -> create MSG_ERROR, player is alive -> Return True
        elif status == PlayerReturnStatus.BALL_OOB :
            content = 'BALL_OOB|'
            if(info[0] == Orientation.DIR_EAST) :
                content += 'EAST'
            elif (info[0] == Orientation.DIR_NORTH) :
                content += 'NORTH'
            elif (info[0] == Orientation.DIR_WEST) :
                content += 'WEST'
            sendSyncError(content, canvas)


### pauseUpdate - react to pause screen update
def pauseUpdate(status, canvas) :
    # Three seconds left until the game starts...
    if status == PauseReturnStatus.DISP_3 :
        # form message
        toSend = PyMessage()
        toSend.src = canvas.data['myName']
        toSend.kind = MsgType.MSG_PAUSE_UPDATE
        toSend.content = '3|' + str(canvas.data['level'].currentLevel + 1)
        toSend.multicast = True
        # send message
        sendMessage(toSend, canvas)
    # Two seconds left until the game starts...
    elif status == PauseReturnStatus.DISP_2 :
        # form message
        toSend = PyMessage()
        toSend.src = canvas.data['myName']
        toSend.kind = MsgType.MSG_PAUSE_UPDATE
        toSend.content = '2|' + str(canvas.data['level'].currentLevel + 1)
        toSend.multicast = True
        # send message
        sendMessage(toSend, canvas)
    # One second left until the game starts...
    elif status == PauseReturnStatus.DISP_1 :
        # form message
        toSend = PyMessage()
        toSend.src = canvas.data['myName']
        toSend.kind = MsgType.MSG_PAUSE_UPDATE
        toSend.content = '1|' + str(canvas.data['level'].currentLevel + 1)
        toSend.multicast = True
        # send message
        sendMessage(toSend, canvas)
    # Time for the game to begin
    elif status == PauseReturnStatus.MOVE_ON :
        (XSPEED, YSPEED) = canvas.data['ball'].randomVelocity()
        # form message
        toSend = PyMessage()
        toSend.src = canvas.data['myName']
        toSend.kind = MsgType.MSG_START_PLAY
        toSend.content = str(XSPEED*FP_MULT) + '|' + str(YSPEED*FP_MULT)
        toSend.multicast = True
        # send message
        sendMessage(toSend, canvas)

def levelUpdate(status, canvas) :
    if status == LevelReturnStatus.COMPLETE :
        canvas.data['ball'].reset()
        canvas.data['currentState'] = State.STATE_PAUSE

    elif status == LevelReturnStatus.GAME_OVER :
        canvas.delete(ALL)
        canvas.data['winner'] = getWinner(canvas);
        canvas.data['currentState'] = State.STATE_GAME_OVER


### redrawAll - draw the game screen
def redrawAll(canvas) :
    receiveAll(canvas)
    gameType = canvas.data['gameType']
    myName = canvas.data['myName']
    currentState = canvas.data['currentState']

    ### SPLASH - get player name
    if currentState == State.STATE_SPLASH :
        # draw screen background and ball
        canvas.data['splashScreen'].drawBackground(canvas)
        canvas.data['ball'].updateMenu(canvas)

        # draw screen foreground and text box AFTER ball so they are over the ball
        canvas.data['splashScreen'].drawText(canvas)
        canvas.data['splashTextField'].draw(canvas)        

    ### MENU - start a game
    elif currentState == State.STATE_MENU :
        # draw screen background and ball
        canvas.data['menuScreen'].drawBackground(canvas)
        canvas.data['ball'].updateMenu(canvas)

        # draw screen foreground and buttons AFTER ball so they are over the ball
        canvas.data['menuScreen'].drawText(canvas)
        canvas.data['soloButton'].draw(canvas)
        canvas.data['joinButton'].draw(canvas)

    ### JOIN - wait for everyone to connect to a multiplayer game
    elif currentState == State.STATE_JOIN :
        canvas.data['joinScreen'].draw(canvas)
        canvas.data['ball'].updateMenu(canvas)

    ### PAUSE SINGLE PLAYER - countdown 
    elif currentState == State.STATE_PAUSE and gameType == GameType.SINGLE_PLAYER :
        # draw screen and ball
        canvas.data['gameScreen'].draw(canvas)
        canvas.data['ball'].draw(canvas)

        # update all players
        for player in canvas.data['competitors'] :
            (status, info) = canvas.data[player].update(canvas)
            playerUpdate(player, status, info, canvas)

        # update the screen to countdown (3...2....1...)
        status = canvas.data['pauseScreen'].draw(canvas)
        if status == PauseReturnStatus.MOVE_ON :
            canvas.data['currentState'] = State.STATE_GAMEPLAY

    ### PAUSE MULTI_PLAYER - send message updates
    elif currentState == State.STATE_PAUSE and gameType == GameType.MULTI_PLAYER :
        # draw screen and ball
        canvas.data['gameScreen'].draw(canvas)
        canvas.data['ball'].draw(canvas)
        # clearMyReceivedFlags(canvas)

        # update all players
        for player in canvas.data['competitors'] :
            (status, info) = canvas.data[player].update(canvas)
            playerUpdate(player, status, info, canvas)

        # update the screen to countdown (3...2....1...)
        status = canvas.data['pauseScreen'].draw(canvas)
        pauseUpdate(status, canvas)

    ### GAMEPLAY SINGLE PLAYER - play the game
    elif currentState == State.STATE_GAMEPLAY and gameType == GameType.SINGLE_PLAYER:
        # draw screen
        canvas.data['gameScreen'].draw(canvas)

        # update all players
        for player in canvas.data['competitors'] :
            (status, info) = canvas.data[player].update(canvas)
            playerUpdate(player, status, info, canvas)

        # update the level and ball AFTER players update to allow for bouncing and breaking
        status = canvas.data['level'].update(canvas)
        canvas.data['ball'].updateGame(canvas)
        levelUpdate(status, canvas)

    ### GAMEPLAY MULTI_PLAYER - send the game messgaes
    elif currentState == State.STATE_GAMEPLAY and (gameType == GameType.MULTI_PLAYER) :
        canvas.data['gameScreen'].draw(canvas)

        # update all players
        competitors = canvas.data['competitors']
        for player in competitors :
            (status, info) = canvas.data[player].update(canvas)
            playerUpdate(player, status, info, canvas)

        # update the level and ball AFTER players update to allow for bouncing and breaking
        status = canvas.data['level'].update(canvas)
        canvas.data['ball'].updateGame(canvas)
        levelUpdate(status, canvas)

    ### REJOIN - allow a node to try and rejoin
    elif currentState == State.STATE_REJOIN :
        canvas.data['gameScreen'].draw(canvas)

        # update the level and ball AFTER players update to allow for bouncing and breaking
        canvas.data['level'].draw(canvas)
        canvas.data['ball'].updateMenu(canvas)  
        canvas.data['rejoinScreen'].draw(canvas)   

        # get the list of missigng nodes 
        missingNodes = canvas.data['missingNodes']

        # make sure there is something in it
        if missingNodes :
            # loop through all nodes
            for missing in missingNodes :
                # update timer and send kill messages
                timerKey = missing + 'Timer'
                if canvas.data[timerKey] <= 0 and myName == canvas.data['unicorn']:
                    sendKillMessage(missing, canvas)
                else :
                    canvas.data[timerKey] -= 1

        # if there is nothing in the missing nodes list then go back to playing the game! 
        elif myName == canvas.data['unicorn'] :
            toSend = PyMessage()
            toSend.src = myName
            toSend.kind = MsgType.MSG_FORCE_COMMIT
            toSend.content = ConType.CON_GAME_STATE + '|' + getGameState(canvas)
            toSend.multicast = True
            # send message
            canvas.data['bridge'].sendMessage(toSend)

    ### SYNC - perform game state consensus to sync everyone up
    elif currentState == State.STATE_SYNC :
        canvas.data['gameScreen'].draw(canvas)

        # update the level and ball AFTER players update to allow for bouncing and breaking
        canvas.data['level'].draw(canvas)
        canvas.data['ball'].updateMenu(canvas)  
        canvas.data['syncScreen'].draw(canvas)   

        if canvas.data['myReceived'][MsgType.MSG_CON_REQ] == True and canvas.data['unicorn'] == myName and canvas.data['artificalSync'] == False :
            toSend = PyMessage()
            toSend.src = myName
            toSend.kind = MsgType.MSG_CON_REQ
            toSend.content = ConType.CON_GAME_STATE + '|' + getGameState(canvas)
            toSend.multicast = False
            sendMessage(toSend, canvas)
            print(myName + " has requested that we perform consensus.")

    # GAME OVER SCREEN
    elif canvas.data['currentState'] == State.STATE_GAME_OVER : 
        canvas.data['gameOverScreen'].draw(canvas);
        canvas.data['ball'].updateMenu(canvas)  

    #  redraw after delay
    canvas.after(DELAY, redrawAll, canvas)     

### init - initialize dictionary
def init(canvas) :
    # current screen
    canvas.data['currentState'] = State.STATE_SPLASH

    # misc
    canvas.data['myName'] = 'Type name...'
    canvas.data['unicorn'] = 'UNSET'
    canvas.data['gameType'] = GameType.UNSET

    ### COMPONENETS
    # buttons
    canvas.data['soloButton'] = Button(X_CENTER, Y_LOC_TOP_BUTTON, 'Solo Game', True)
    canvas.data['joinButton'] = Button(X_CENTER, Y_LOC_BOTTOM_BUTTON, 'Join Game', True)

    # ball
    canvas.data['ball'] = Ball()

    # screens
    canvas.data['gameScreen']   = GameScreen()
    canvas.data['gameOverScreen'] = GameOverScreen()  
    canvas.data['joinScreen']   = JoinScreen()  
    canvas.data['menuScreen']   = MenuScreen()
    canvas.data['pauseScreen']  = PauseScreen()
    canvas.data['rejoinScreen'] = RejoinScreen()
    canvas.data['syncScreen']   = SyncScreen() 
    canvas.data['splashScreen'] = SplashScreen()

    canvas.data['playersInitialized'] = False
    canvas.data['attemptingRejoin'] = False
    canvas.data['artificalSync'] = False
    canvas.data['artificialDead'] = False

    canvas.data['missingNodes'] = []

    # screen objects
    canvas.data['splashTextField'] = TextField(X_CENTER, Y_LOC_TOP_BUTTON, 'Type name...', L_TEXT_SIZE)
    canvas.data['level'] = Level()

    canvas.data['myReceived'] = {}
    clearMyReceivedFlags(canvas)

### initPlayers - initialize players
def initPlayers(canvas, number=1, info=[]):
    myName = canvas.data['myName']
    if canvas.data['gameType'] == GameType.SINGLE_PLAYER: 
        canvas.data[myName] = Player(Orientation.DIR_SOUTH, PlayerState.USER, myName, GameType.SINGLE_PLAYER)
        canvas.data['armin'] = Player(Orientation.DIR_NORTH, PlayerState.AI, 'armin', GameType.MULTI_PLAYER)
        canvas.data['lunwen'] = Player(Orientation.DIR_EAST, PlayerState.AI, 'lunwen', GameType.MULTI_PLAYER)
        canvas.data['garrett'] = Player(Orientation.DIR_WEST, PlayerState.AI, 'garrett', GameType.MULTI_PLAYER)
        canvas.data['competitors'] = [myName, 'armin', 'lunwen', 'garrett']
        canvas.data['playersInitialized'] = True
    
    elif canvas.data['gameType'] == GameType.MULTI_PLAYER: 
        # create my player
        canvas.data[myName] = Player(Orientation.DIR_SOUTH, PlayerState.USER, myName, GameType.MULTI_PLAYER)

        # update info array for a three player game
        ### Basically, add a wall in the fourth slot in the info array.
        if number == 3:
            # add a wall to the index array
            w = random.randint(0, len(WALL_NAMES)-1)
            info.append(WALL_NAMES[w])

        # update info array for a two player game
        ### If players A and B were receieved in the info array, update the info array to look like:
        ###     [A, WALL1, B, WALL2]
        if number == 2:
            w1 = random.randint(0, len(WALL_NAMES)-1)
            w2 = w1
            while w2 == w1 :
                w2 = random.randint(0, len(WALL_NAMES)-1)
            info = [info[0], WALL_NAMES[w1], info[1], WALL_NAMES[w2]]

        # get other players index in the info array
        myIndex = info.index(myName)
        eastIndex = (myIndex + 1) % 4
        northIndex = (myIndex + 2) % 4
        westIndex = (myIndex + 3) % 4

        # set level orientaion based on odering of the players. 
        ### WHAT THE HECK DOES THIS MEAN: 
        ### Okay. Everyone is going to see themselves on the bottom of their screen. So...
        ###     Translating the ball position and the paddle position send by other players is
        ###     relatively easy because it does not require a global notion of orientation, you
        ###     need only know where a player is RELATIVE to you. However, there has got to be an
        ###     anchor for drawing a level. The natural notion is, 'Easy! Have the unicorn be the
        ###     anchor!!!', but it would behoove us to do something deterministic. SO. The player
        ###     that gets sent out first, which is to say the player that comes first alphabetically,
        ###     get's to be the anchor. </rant>
        if myIndex == 0 :
            canvas.data[myName].levelOrientation = Orientation.DIR_SOUTH
            canvas.data['level'].levelOrientation = Orientation.DIR_SOUTH     
        elif myIndex == 1 :
            canvas.data[myName].levelOrientation = Orientation.DIR_EAST
            canvas.data['level'].levelOrientation = Orientation.DIR_EAST    
        elif myIndex == 2 :
            canvas.data[myName].levelOrientation = Orientation.DIR_NORTH
            canvas.data['level'].levelOrientation = Orientation.DIR_NORTH
        elif myIndex == 3 :
            canvas.data[myName].levelOrientation = Orientation.DIR_WEST
            canvas.data['level'].levelOrientation = Orientation.DIR_WEST        

        # make EAST player appropriately
        if info[eastIndex] in WALL_NAMES :
            canvas.data[info[eastIndex]] = Player(Orientation.DIR_EAST, PlayerState.WALL, info[eastIndex], GameType.MULTI_PLAYER)
        else :
            canvas.data[info[eastIndex]] = Player(Orientation.DIR_EAST, PlayerState.COMP, info[eastIndex], GameType.MULTI_PLAYER)

        # make WEST player appropriately
        if info[northIndex] in WALL_NAMES :
            canvas.data[info[northIndex]] = Player(Orientation.DIR_NORTH, PlayerState.WALL, info[northIndex], GameType.MULTI_PLAYER)
        else :
            canvas.data[info[northIndex]] = Player(Orientation.DIR_NORTH, PlayerState.COMP, info[northIndex], GameType.MULTI_PLAYER)

        if info[westIndex] in WALL_NAMES :
            canvas.data[info[westIndex]] = Player(Orientation.DIR_WEST, PlayerState.WALL, info[westIndex], GameType.MULTI_PLAYER) 
        else :   
            canvas.data[info[westIndex]] = Player(Orientation.DIR_WEST, PlayerState.COMP, info[westIndex], GameType.MULTI_PLAYER)    
        
        # save competitor information
        canvas.data['competitors'] = info 
        canvas.data['playersInitialized'] = True       

### run - run the program
def runUI(cmd_line_args) :

    def on_closing() :
        toSend = PyMessage()
        toSend.src = canvas.data['myName']
        toSend.kind = MsgType.MSG_EXIT
        toSend.content = 'MISFITS_RULE'
        toSend.multicast = True
        # send message
        canvas.data['bridge'].sendMessage(toSend)
        root.destroy()


    # initialize canvas
    root = Tk()
    canvas = Canvas(root, width=CANVAS_WIDTH, height= CANVAS_HEIGHT, background='white')
    canvas.pack()

    # make it so the window is not resizable
    root.resizable(height = 0, width = 0)

    # give the canvas a title
    root.title('Multegula')

    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # set up dicitonary
    canvas.data = {}

    # sets up events
    root.bind('<Button-1>', mousePressed)
    root.bind('<Key>', keyPressed)

    # get the GoBridge
    canvas.data['bridge'] = GoBridge(cmd_line_args[1]);
    
    # Set up for ReceiveThread
    Process = threading.Thread(target=canvas.data['bridge'].receiveThread)
    Process.start()

    # let the games begin
    init(canvas)
    redrawAll(canvas)
    root.mainloop()

    Process.join()
    sys.exit(2)

#Start UI
runUI(sys.argv)
