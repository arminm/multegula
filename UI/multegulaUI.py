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
from UI.components.screens.SplashScreen import *
from UI.components.screens.MenuScreen import *
from UI.components.screens.PauseScreen import *
from UI.components.screens.GameOver import *
from UI.components.screens.GameScreen import *
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
            canvas.data['playerName'] = canvas.data['splashTextField'].text

    # pause screen / gameplay keyPressed events - move the paddle
    elif (currentScreen == Screens.SCRN_PAUSE) or (currentScreen == Screens.SCRN_GAME) :
        if (event.keysym == 'Left') or (event.keysym == 'a') or (event.keysym == 'A') :
            canvas.data['Player_01'].paddle.direction = Direction.DIR_LEFT
        elif (event.keysym == 'Right') or (event.keysym == 'd') or (event.keysym == 'D') :
            canvas.data['Player_01'].paddle.direction = Direction.DIR_RIGHT

### keyReleased - handle key release events
def keyReleased(event) :
    canvas = event.widget.canvas
    currentScreen = canvas.data['currentScreen']

    # pause screen / gameplay keyReleased events - stop paddle motion
    if (currentScreen == Screens.SCRN_PAUSE) or (currentScreen == Screens.SCRN_GAME) :
        if((event.keysym == 'Left') or (event.keysym == 'a') or (event.keysym == 'A') or 
            (event.keysym == 'Right') or (event.keysym == 'd') or (event.keysym == 'D')) :
            canvas.data['Player_01'].paddle.direction = Direction.DIR_STOP

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
            initPlayers(canvas)

            # initialize game
            canvas.data['currentScreen'] = Screens.SCRN_GAME
            canvas.data['ball'].reset()
            canvas.delete(ALL)

    # game over screen mouse pressed events - start over
    elif canvas.data['currentScreen'] == Screens.SCRN_GAME_OVER :
        init(canvas);


def receiveAndReact(canvas) :
    bridge = canvas.data['bridge']

    # this emulates a do-while loop
    while True:
        message = bridge.receiveMessage()

        if message.src == '':
            break
        else:
            print("UI: " + message.printMessage())

### redrawAll - draw the game screen
def redrawAll(canvas) :
    receiveAndReact(canvas)

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

    ### PAUSE SCREEN
    elif canvas.data['currentScreen'] == Screens.SCRN_PAUSE :
        canvas.data['gameScreen'].draw(canvas)
        canvas.data['ball'].draw(canvas)
        canvas.data['Player_01'].update(canvas)
        canvas.data['Player_02'].update(canvas)
        canvas.data['Player_03'].update(canvas)
        canvas.data['Player_04'].update(canvas)
        canvas.data['pauseScreen'].draw(canvas)

    ### GAME SCREEN
    elif (canvas.data['currentScreen'] == Screens.SCRN_GAME) and (canvas.data['gameType'] == GameType.SINGLE_PLAYER):
        canvas.data['gameScreen'].draw(canvas)
        canvas.data['Player_01'].update(canvas)
        canvas.data['Player_02'].update(canvas)
        canvas.data['Player_03'].update(canvas)
        canvas.data['Player_04'].update(canvas)
        canvas.data['level'].update(canvas)
        canvas.data['ball'].updateGame(canvas)

    elif (canvas.data['currentScreen'] == Screens.SCRN_GAME) and (canvas.data['gameType'] == GameType.MULTI_PLAYER):
        canvas.data['gameScreen'].draw(canvas)
        canvas.data['Player_01'].update(canvas)
        canvas.data['Player_02'].update(canvas)
        canvas.data['Player_03'].update(canvas)
        canvas.data['Player_04'].update(canvas)
        canvas.data['level'].update(canvas)

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
    canvas.data['playerName'] = 'Type name...'

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

    # screen objects
    canvas.data['splashTextField'] = TextField(X_CENTER, Y_LOC_TOP_BUTTON, 'Type name...', L_TEXT_SIZE)
    canvas.data['level'] = Level()

def initPlayers(canvas):
    if canvas.data['gameType'] == GameType.SINGLE_PLAYER: 
        canvas.data['Player_01'] = Player(Orientation.DIR_SOUTH, PlayerState.USER, canvas.data['playerName'], GameType.SINGLE_PLAYER)
        canvas.data['Player_02'] = Player(Orientation.DIR_NORTH, PlayerState.AI, 'NoRTH', GameType.SINGLE_PLAYER)
        canvas.data['Player_03'] = Player(Orientation.DIR_EAST, PlayerState.AI, 'eaST', GameType.SINGLE_PLAYER)
        canvas.data['Player_04'] = Player(Orientation.DIR_WEST, PlayerState.AI, 'WeST', GameType.SINGLE_PLAYER)
    
    elif canvas.data['gameType'] == GameType.MULTI_PLAYER: 
        canvas.data['Player_01'] = Player(Orientation.DIR_SOUTH, PlayerState.USER, canvas.data['playerName'], GameType.MULTI_PLAYER)
        canvas.data['Player_02'] = Player(Orientation.DIR_NORTH, PlayerState.COMP, 'NoRTH', GameType.MULTI_PLAYER)
        canvas.data['Player_03'] = Player(Orientation.DIR_EAST, PlayerState.COMP, 'eaST', GameType.MULTI_PLAYER)
        canvas.data['Player_04'] = Player(Orientation.DIR_WEST, PlayerState.COMP, 'WeST', GameType.MULTI_PLAYER) 

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

    # act on command line arguments
    if (len(cmd_line_args) > 1) and (cmd_line_args[1] == '-mid'):
        canvas.data['mid_demo'] = True;
    else:
        canvas.data['mid_demo'] = False;

    # sets up events
    #root.bind('<Key>', keyPressed)
    root.bind('<Button-1>', mousePressed)
    root.bind('<Key>', keyPressed)
    root.bind('<KeyRelease>', keyReleased)

    # get the GoBridge
    canvas.data['bridge'] = GoBridge();
    
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
