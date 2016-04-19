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
from bridges.GoBridge import * #This is our GoBridge
import threading #To run receiveThread
from UI.components.control.Level import *
from UI.components.control.Player import *
from UI.components.gameplay.Ball import *
from UI.components.gameplay.Block import *
from UI.components.gameplay.Paddle import *
from UI.components.directive.Button import *
from UI.components.directive.TextField import *
from UI.components.screens.GameOver import *
from UI.components.screens.GameScreen import *
from UI.components.screens.JoinScreen import *
from UI.components.screens.MenuScreen import *
from UI.components.screens.PauseScreen import *
from UI.components.screens.SplashScreen import *
from UI.typedefs import *

### keyPressed - handle keypressed events
def keyPressed(event) :
    canvas = event.widget.canvas
    currentScreen = canvas.data['currentScreen']

    # handle splash screen events - entering a name
    if(currentScreen == Screens.SCRN_SPLASH) :
        # add new characters
        if '!' <= event.char <= 'z' :
            canvas.data['splashTextField'].addChar(event.char)            
        # remove characters
        elif event.keysym == 'BackSpace' :
            canvas.data['splashTextField'].deleteChar()            
        # addd space 
        elif event.keysym == 'space' :
            canvas.data['splashTextField'].addChar(' ')            
        # enter the name
        elif (event.keysym == 'Return') and canvas.data['splashTextField'].changed :
            canvas.data['currentScreen'] = Screens.SCRN_MENU
            # set name
            myName = canvas.data['splashTextField'].text
            canvas.data['myName'] = myName

            # send name up to Multegula!
            toSend = PyMessage()
            toSend.src = myName
            toSend.kind = MsgType.MSG_MYNAME
            toSend.content = myName
            toSend.multicast = False
            canvas.data['bridge'].sendMessage(toSend)

    # pause screen / gameplay keyPressed events - move the paddle
    elif (currentScreen == Screens.SCRN_PAUSE) or (currentScreen == Screens.SCRN_GAME) :
        myName  = canvas.data['myName']
        myPaddle = canvas.data[myName].paddle

        ### MOVE PADDLE LEFT ###
        if (event.keysym == 'Left') or (event.keysym == 'a') or (event.keysym == 'A') :
            # if this is a multi-player game, the direction is not already set, and the paddle can move,
            #   then it is okay to send an update
            if canvas.data['gameType'] == GameType.MULTI_PLAYER:
                if myPaddle.direction != Direction.DIR_LEFT and myPaddle.canMove(Direction.DIR_LEFT):
                    # create and send message
                    toSend = PyMessage()
                    toSend.src =  myName
                    toSend.kind = MsgType.MSG_PADDLE_DIR
                    toSend.content = MsgPayload.PADDLE_DIR_LEFT
                    toSend.multicast = True
                    canvas.data['bridge'].sendMessage(toSend)

            # if this is a single player game, then go ahead and set the paddle direction
            elif canvas.data['gameType'] == GameType.SINGLE_PLAYER: 
                myPaddle.direction = Direction.DIR_LEFT

        ### MOVE PADDLE RIGHT ####
        elif (event.keysym == 'Right') or (event.keysym == 'd') or (event.keysym == 'D') :
            # if this is a multi-player game, the direction is not already set, and the paddle can move,
            #   then it is okay to send an update.  
            if canvas.data['gameType'] == GameType.MULTI_PLAYER: 
                if myPaddle.direction != Direction.DIR_RIGHT and myPaddle.canMove(Direction.DIR_RIGHT):
                    # create and send message
                    toSend = PyMessage()
                    toSend.src = myName
                    toSend.kind = MsgType.MSG_PADDLE_DIR
                    toSend.content = MsgPayload.PADDLE_DIR_RIGHT
                    toSend.multicast = True
                    canvas.data['bridge'].sendMessage(toSend)

            # if this is a single player game, then go ahead and set the paddle direction
            elif canvas.data['gameType'] == GameType.SINGLE_PLAYER: 
                canvas.data[canvas.data['myName']].paddle.direction = Direction.DIR_RIGHT


### keyReleased - handle key release events
def keyReleased(event) :
    canvas = event.widget.canvas
    currentScreen = canvas.data['currentScreen']

    ### STOP PADDLE MOTION ###
    if (currentScreen == Screens.SCRN_PAUSE) or (currentScreen == Screens.SCRN_GAME) :
        if((event.keysym == 'Left') or (event.keysym == 'a') or (event.keysym == 'A') or 
            (event.keysym == 'Right') or (event.keysym == 'd') or (event.keysym == 'D')) :

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
                    toSend.kind = MsgType.MSG_PADDLE_POS
                    toSend.content = str(CENTER) + '|' + str(WIDTH)
                    toSend.multicast = True
                    canvas.data['bridge'].sendMessage(toSend)

            # if this is a single player game, then go ahead and set the paddle direction
            elif canvas.data['gameType'] == GameType.SINGLE_PLAYER: 
                canvas.data[canvas.data['myName']].paddle.direction = Direction.DIR_STOP


### mousePressed - handle mouse press events
def mousePressed(event) :
    canvas = event.widget.canvas

    # main screen mouse pressed events - button clicks
    if canvas.data['currentScreen'] == Screens.SCRN_MENU : 
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
            canvas.data['bridge'].sendMessage(toSend)

            # initialize game
            canvas.data['currentScreen'] = Screens.SCRN_PAUSE
            canvas.data['nextScreen'] = Screens.SCRN_GAME

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
            canvas.data['bridge'].sendMessage(toSend)

            # initialize game
            canvas.data['currentScreen'] = Screens.SCRN_JOIN
            canvas.data['ball'].reset()
            canvas.delete(ALL)

    # game over screen mouse pressed events - start over
    elif canvas.data['currentScreen'] == Screens.SCRN_GAME_OVER :
        init(canvas);


def react(canvas, received) :
    # break down message
    kind = received.kind
    name = received.src
    content = received.content
    myName = canvas.data['myName']
    print(myName + " Received: " + received.toString())

    if kind == MsgType.MSG_PLAYER_LOC :
        initPlayers(canvas, int(content[0]), content[1:])
        canvas.data['currentScreen'] = Screens.SCRN_PAUSE
        canvas.data['nextScreen'] = Screens.SCRN_GAME

    # MSG_PADDLE_DIR
    elif kind == MsgType.MSG_PADDLE_DIR :
        print(myName + " paddle dir...")
        if content[MsgIndex.PADDLE_DIR] == MsgPayload.PADDLE_DIR_LEFT:
            print(myName + " left...")
            canvas.data[name].paddle.direction = Direction.DIR_LEFT
        elif content[MsgIndex.PADDLE_DIR] == MsgPayload.PADDLE_DIR_RIGHT:
            print(myName + " right...")
            canvas.data[name].paddle.direction = Direction.DIR_RIGHT

    # MSG_PADDLE_POS
    elif kind == MsgType.MSG_PADDLE_POS : 
        canvas.data[name].paddle.direction = Direction.DIR_STOP
        canvas.data[name].paddle.center = int(content[MsgIndex.PADDLE_POS_CENTER])
        canvas.data[name].paddle.width = int(content[MsgIndex.PADDLE_POS_WIDTH])

    # MSG_BALL_MISSED
    elif kind == MsgType.MSG_BALL_MISSED : 
        canvas.data[name].score = int(content[MsgIndex.BALL_MISSED_SCORE])
        canvas.data[name].lives = int(content[MsgIndex.BALL_MISSED_LIVES])
        canvas.data[name].statusUpdate = True
        canvas.data['ball'].reset()
        canvas.data['currentScreen'] = Screens.SCRN_PAUSE
        canvas.data['nextScreen'] = Screens.SCRN_GAME

    # MSG_BALL_DEFLECTED
    elif kind == MsgType.MSG_BALL_DEFLECTED :
        canvas.data[name].score = int(content[MsgIndex.BALL_DEFLECTED_SCORE])
        canvas.data[name].statusUpdate = True
        canvas.data['ball'].lastToTouch = name
        canvas.data['ball'].setCenter(float(content[MsgIndex.BALL_DEFLECTED_XCENTER]) / FP_MULT, float(content[MsgIndex.BALL_DEFLECTED_YCENTER]) / FP_MULT)
        canvas.data['ball'].radius = float(content[MsgIndex.BALL_DEFLECTED_RADIUS]) / FP_MULT
        canvas.data['ball'].setVelocity(float(content[MsgIndex.BALL_DEFLECTED_XSPEED]) / FP_MULT, float(content[MsgIndex.BALL_DEFLECTED_YSPEED]) / FP_MULT)
        canvas.data['ball'].randomColor()

    # MSG_BLOCK_BROKEN
    elif kind == MsgType.MSG_BLOCK_BROKEN :
        canvas.data[name].score = int(content[MsgIndex.BLOCK_BROKEN_SCORE])
        canvas.data[name].lives = int(content[MsgIndex.BLOCK_BROKEN_LIVES])  
        canvas.data[name].statusUpdate = True
        canvas.data['ball'].lastToTouch = name
        canvas.data['ball'].setCenter(float(content[MsgIndex.BLOCK_BROKEN_XCENTER]) / FP_MULT, float(content[MsgIndex.BLOCK_BROKEN_YCENTER]) / FP_MULT)
        canvas.data['ball'].radius = float(content[MsgIndex.BLOCK_BROKEN_RADIUS]) / FP_MULT
        canvas.data['ball'].setVelocity(int(content[MsgIndex.BLOCK_BROKEN_XSPEED]) / FP_MULT, float(content[MsgIndex.BLOCK_BROKEN_YSPEED]) / FP_MULT)
        canvas.data['ball'].randomColor()
        canvas.data['level'].blocks[int(content[MsgIndex.BLOCK_BROKEN_BLOCK])].disable()
        canvas.data['level'].updated = True

### receiveAll - get all messages from the GoBrige
def receiveAll(canvas) :
    # loop until there are no
    while True:
        message = canvas.data['bridge'].receiveMessage();
        if message.src == '':
            break
        else:
            react(canvas, message)

def playerUpdate(name, status, info, canvas) :
    # single player game -> directly update appropriate game information
    if canvas.data['gameType'] == GameType.SINGLE_PLAYER :
        # ball missed -> update status and reset
        if status == PlayerReturnStatus.BALL_MISSED :
            canvas.data[name].score += LOST_LIFE_POINTS
            canvas.data[name].lives += LOST_LIFE_LIVES
            canvas.data[name].statusUpdate = True
            canvas.data['ball'].reset()
            canvas.data['currentScreen'] = Screens.SCRN_PAUSE
            canvas.data['nextScreen'] = Screens.SCRN_GAME

        # ball deflected -> update status and set ball properties
        elif status == PlayerReturnStatus.BALL_DEFLECTED :
            canvas.data[name].score += DEFLECT_POINTS
            canvas.data[name].statusUpdate = True
            canvas.data['ball'].lastToTouch = name;    
            canvas.data['ball'].setVelocity(info[0], info[1])  
            canvas.data['ball'].randomColor()
        
        # block broken -> update status, set ball properties, update level
        elif status == PlayerReturnStatus.BLOCK_BROKEN :
            canvas.data[name].score += BREAK_POINTS;    
            canvas.data[name].statusUpdate = True
            canvas.data['ball'].setVelocity(info[0], info[1])  
            canvas.data['level'].blocks[info[2]].disable()
            canvas.data['level'].updated = True

    # multiplayer game -> send update to competitors
    elif canvas.data['gameType'] == GameType.MULTI_PLAYER :

        # ball missed -> created MSG_BALL_MISSED
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
            canvas.data['bridge'].sendMessage(toSend)

        # ball deflected -> create MSG_BALL_DEFLECTED
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
            canvas.data['bridge'].sendMessage(toSend)

        elif status == PlayerReturnStatus.WALL_BALL_DEFLECTED :
            canvas.data['ball'].setVelocity(info[0], info[1])  
            canvas.data['ball'].randomColor()

        # block broken -> create MSG_BLOCK_BROKEN
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
            canvas.data['bridge'].sendMessage(toSend)


### redrawAll - draw the game screen
def redrawAll(canvas) :
    receiveAll(canvas)

    ### SPLASH SCREEN
    if canvas.data['currentScreen'] == Screens.SCRN_SPLASH :
        canvas.data['splashScreen'].drawBackground(canvas)
        canvas.data['ball'].updateMenu(canvas)
        canvas.data['splashScreen'].drawText(canvas)
        canvas.data['splashTextField'].draw(canvas)        

    ### MAIN SCREEN 
    elif canvas.data['currentScreen'] == Screens.SCRN_MENU :
        canvas.data['menuScreen'].drawBackground(canvas)
        canvas.data['ball'].updateMenu(canvas)
        canvas.data['menuScreen'].drawText(canvas)
        canvas.data['soloButton'].draw(canvas)
        canvas.data['joinButton'].draw(canvas)

    elif canvas.data['currentScreen'] == Screens.SCRN_JOIN :
        canvas.data['joinScreen'].draw(canvas)

    ### PAUSE SCREEN
    elif canvas.data['currentScreen'] == Screens.SCRN_PAUSE :
        canvas.data['gameScreen'].draw(canvas)
        canvas.data['ball'].draw(canvas)
        # canvas.data[canvas.data['myName']].update(canvas)
        for player in canvas.data['competitors'] :
            (status, info) = canvas.data[player].update(canvas)
            playerUpdate(player, status, info, canvas)

        canvas.data['pauseScreen'].draw(canvas)

    ### GAME SCREEN
    elif (canvas.data['currentScreen'] == Screens.SCRN_GAME) and (canvas.data['gameType'] == GameType.SINGLE_PLAYER):
        canvas.data['gameScreen'].draw(canvas)

        # update all other players
        for player in canvas.data['competitors'] :
            (status, info) = canvas.data[player].update(canvas)
            playerUpdate(player, status, info, canvas)

        canvas.data['level'].update(canvas)
        canvas.data['ball'].updateGame(canvas)

    elif (canvas.data['currentScreen'] == Screens.SCRN_GAME) and (canvas.data['gameType'] == GameType.MULTI_PLAYER):
        canvas.data['gameScreen'].draw(canvas)

        competitors = canvas.data['competitors']
        for player in competitors :
            (status, info) = canvas.data[player].update(canvas)
            playerUpdate(player, status, info, canvas)

        canvas.data['level'].update(canvas)
        ##canvas.data['ball'].updateGame(canvas)


    # GAME OVER SCREEN
    elif canvas.data['currentScreen'] == Screens.SCRN_GAME_OVER : 
        canvas.data['gameOverScreen'].draw(canvas);

    #  redraw after delay
    canvas.after(canvas.data['delay'], redrawAll, canvas)     

### init - initialize dictionary
def init(canvas) :
    # current screen
    canvas.data['currentScreen'] = Screens.SCRN_SPLASH
    canvas.data['nextScreen'] = Screens.SCRN_NONE

    # misc
    canvas.data['delay'] = 10
    canvas.data['myName'] = 'Type name...'

    ### COMPONENETS
    # buttons
    canvas.data['soloButton'] = Button(X_CENTER, Y_LOC_TOP_BUTTON, 'Solo Game', True)
    canvas.data['joinButton'] = Button(X_CENTER, Y_LOC_BOTTOM_BUTTON, 'Join Game', True)

    # ball
    canvas.data['ball'] = Ball()

    # screens
    canvas.data['gameScreen']   = GameScreen()
    canvas.data['menuScreen']   = MenuScreen()
    canvas.data['pauseScreen']  = PauseScreen()
    canvas.data['splashScreen'] = SplashScreen()
    canvas.data['gameOverScreen'] = GameOver()  
    canvas.data['joinScreen']   = JoinScreen()  

    # screen objects
    canvas.data['splashTextField'] = TextField(X_CENTER, Y_LOC_TOP_BUTTON, 'Type name...', L_TEXT_SIZE)
    canvas.data['level'] = Level()

def initPlayers(canvas, number=1, info=[]):
    myName = canvas.data['myName']
    if canvas.data['gameType'] == GameType.SINGLE_PLAYER: 
        canvas.data[myName] = Player(Orientation.DIR_SOUTH, PlayerState.USER, myName, GameType.SINGLE_PLAYER)
        canvas.data['armin'] = Player(Orientation.DIR_NORTH, PlayerState.AI, 'armin', GameType.MULTI_PLAYER)
        canvas.data['lunwen'] = Player(Orientation.DIR_EAST, PlayerState.AI, 'lunwen', GameType.MULTI_PLAYER)
        canvas.data['garrett'] = Player(Orientation.DIR_WEST, PlayerState.AI, 'garrett', GameType.MULTI_PLAYER)
        canvas.data['competitors'] = [myName, 'armin', 'lunwen', 'garrett']
    
    elif canvas.data['gameType'] == GameType.MULTI_PLAYER: 
        canvas.data[myName] = Player(Orientation.DIR_SOUTH, PlayerState.USER, myName, GameType.MULTI_PLAYER)
        myIndex = info.index(myName);
        if number == 4 :
            eastIndex = (myIndex + 1) % 4
            northIndex = (myIndex + 2) % 4
            westIndex = (myIndex + 3) % 4

            canvas.data[info[eastIndex]] = Player(Orientation.DIR_EAST, PlayerState.COMP, info[eastIndex], GameType.MULTI_PLAYER)
            canvas.data[info[northIndex]] = Player(Orientation.DIR_NORTH, PlayerState.COMP, info[northIndex], GameType.MULTI_PLAYER)
            canvas.data[info[westIndex]] = Player(Orientation.DIR_WEST, PlayerState.COMP, info[westIndex], GameType.MULTI_PLAYER)
            canvas.data['competitors'] = info

### run - run the program
def runUI(cmd_line_args) :

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

    # set up dicitonary
    canvas.data = {}

    # sets up events
    #root.bind('<Key>', keyPressed)
    root.bind('<Button-1>', mousePressed)
    root.bind('<Key>', keyPressed)
    root.bind('<KeyRelease>', keyReleased)

    # get the GoBridge
    #TODO: MAKE THIS MORE ROBUST.  CHECK TO ENSURE A PORT AND NOT "-mid" WAS PASSED IN.
    canvas.data['bridge'] = GoBridge(cmd_line_args[1]);
    
    # Set up for ReceiveThread
    Process = threading.Thread(target=canvas.data['bridge'].receiveThread)
    Process.start()

    # let the games begin
    init(canvas)
    redrawAll(canvas)
    root.mainloop()

    #Properly close receiveThread
    Process.join()

#Start UI
runUI(sys.argv)
