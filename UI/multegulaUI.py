# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# multegulaUI.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

#Tells Python to search Bridges folder for functions as well.
import sys
sys.path.append('../Bridges/')

# imports
from tkinter import *
import random
from components.Ball import *
from components.Block import *
from components.Button import *
from components.Paddle import *
from components.Player import *
from components.TextField import *
from components.ComponentDefs import *
from screens.SplashScreen import *
from screens.MenuScreen import *
from screens.PauseScreen import *
from screens.ScreenEnum import *
from screens.GameOver import *
from screens.GameScreen import *
from levels.Level import *
#from Bridges.GoBridge import * #This is our GoBridge

### keyPressed - handle keypressed events
def keyPressed(event) :
    canvas = event.widget.canvas
    currentScreen = canvas.data["currentScreen"]

    # handle splash screen events - entering a name
    if(currentScreen == Screens.SCRN_SPLASH) :
        # add new characters
        if "!" <= event.char <= "z" :
            canvas.data["splashTextField"].addChar(event.char)            
        # remove characters
        elif event.keysym == "BackSpace" :
            canvas.data["splashTextField"].deleteChar()            
        # addd space 
        elif event.keysym == "space" :
            canvas.data["splashTextField"].addChar(" ")            
        # enter the name
        elif (event.keysym == "Return") and canvas.data["splashTextField"].changed :
            canvas.data["currentScreen"] = Screens.SCRN_MENU
            # set name
            canvas.data["Player_01"].name = canvas.data["splashTextField"].text

    # pause screen / gameplay keyPressed events - move the paddle
    elif (currentScreen == Screens.SCRN_PAUSE) or (currentScreen == Screens.SCRN_GAME) :
        if (event.keysym == "Left") or (event.keysym == "a") or (event.keysym == "A") :
            canvas.data["Player_01"].paddle.direction = Direction.DIR_LEFT
        elif (event.keysym == "Right") or (event.keysym == "d") or (event.keysym == "D") :
            canvas.data["Player_01"].paddle.direction = Direction.DIR_RIGHT

### keyReleased - handle key release events
def keyReleased(event) :
    canvas = event.widget.canvas
    currentScreen = canvas.data["currentScreen"]

    # pause screen / gameplay keyReleased events - stop paddle motion
    if (currentScreen == Screens.SCRN_PAUSE) or (currentScreen == Screens.SCRN_GAME) :
        if((event.keysym == "Left") or (event.keysym == "a") or (event.keysym == "A") or 
            (event.keysym == "Right") or (event.keysym == "d") or (event.keysym == "D")) :
            canvas.data["Player_01"].paddle.direction = Direction.DIR_STOP

### mousePressed - handle mouse press events
def mousePressed(event) :
    canvas = event.widget.canvas

    # main screen mouse pressed events - button clicks
    if canvas.data["currentScreen"] == Screens.SCRN_MENU : 
        if canvas.data["soloButton"].clicked(event.x, event.y) :
            canvas.data["currentScreen"] = Screens.SCRN_PAUSE
            canvas.data["nextScreen"] = Screens.SCRN_GAME
            canvas.data["ball"].reset()
            canvas.delete(ALL)
        elif canvas.data["joinButton"].clicked(event.x, event.y) :
            print("JOIN")

    # game over screen mouse pressed events - start over
    elif canvas.data["currentScreen"] == Screens.SCRN_GAME_OVER :
        init(canvas);

### redrawAll - draw the game screen
def redrawAll(canvas) :
    Y_LOC_TOP_BUTTON = canvas.data["Y_LOC_TOP_BUTTON"]
    X_CENTER  = CANVAS_WIDTH // 2

    ### SPLASH SCREEN
    if canvas.data["currentScreen"] == Screens.SCRN_SPLASH :
        canvas.data["splashScreen"].drawBackground(canvas)
        canvas.data["ball"].updateMenu(canvas)
        canvas.data["splashScreen"].drawText(canvas)
        canvas.data["splashTextField"].draw(canvas)        

    ### MAIN SCREEN 
    elif canvas.data["currentScreen"] == Screens.SCRN_MENU :
        canvas.data["menuScreen"].drawBackground(canvas)
        canvas.data["ball"].updateMenu(canvas)
        canvas.data["menuScreen"].drawText(canvas)
        canvas.data["soloButton"].draw(canvas)
        canvas.data["joinButton"].draw(canvas)

    ### PAUSE SCREEN
    elif canvas.data["currentScreen"] == Screens.SCRN_PAUSE :
        canvas.data["gameScreen"].draw(canvas)
        canvas.data["ball"].draw(canvas)
        canvas.data["Player_01"].update(canvas)
        canvas.data["Player_02"].update(canvas)
        canvas.data["Player_03"].update(canvas)
        canvas.data["Player_04"].update(canvas)
        canvas.data["pauseScreen"].draw(canvas)

    ### GAME SCREEN
    elif canvas.data["currentScreen"] == Screens.SCRN_GAME :
        canvas.data["gameScreen"].draw(canvas)
        canvas.data["Player_01"].update(canvas)
        canvas.data["Player_02"].update(canvas)
        canvas.data["Player_03"].update(canvas)
        canvas.data["Player_04"].update(canvas)
        canvas.data["level"].update(canvas)
        canvas.data["ball"].updateGame(canvas)

    # GAME OVER SCREEN
    elif canvas.data["currentScreen"] == Screens.SCRN_GAME_OVER : 
        canvas.data["gameOverScreen"].draw(canvas);



    #  redraw after delay
    canvas.after(canvas.data["delay"], redrawAll, canvas)


### init - initialize dictionary
def init(canvas) :
    # location constants
    canvas.data["Y_LOC_TOP_BUTTON"] = 0.70*CANVAS_HEIGHT
    canvas.data["Y_LOC_BOTTOM_BUTTON"] = 0.85*CANVAS_HEIGHT
    Y_LOC_TOP_BUTTON = canvas.data["Y_LOC_TOP_BUTTON"]
    Y_LOC_BOTTOM_BUTTON = canvas.data["Y_LOC_BOTTOM_BUTTON"]

    X_MARGIN = CANVAS_WIDTH // 30
    Y_MARGIN = CANVAS_HEIGHT // 30

    # current screen
    canvas.data["currentScreen"] = Screens.SCRN_SPLASH
    canvas.data["nextScreen"] = Screens.SCRN_NONE

    # misc
    canvas.data["delay"] = 10
    canvas.data["playerName"] = "Type name..."

    ### COMPONENETS
    # buttons
    canvas.data["soloButton"] = Button(X_CENTER, Y_LOC_TOP_BUTTON, "Solo Game", True)
    canvas.data["joinButton"] = Button(X_CENTER, Y_LOC_BOTTOM_BUTTON, "Join Game", False)

    # ball
    canvas.data["ball"] = Ball()

    # screens
    canvas.data["gameScreen"]   = GameScreen()
    canvas.data["menuScreen"]   = MenuScreen()
    canvas.data["pauseScreen"]  = PauseScreen()
    canvas.data["splashScreen"] = SplashScreen()
    canvas.data["gameOverScreen"] = GameOver()

    # players
    canvas.data["Player_01"] = Player(Orientation.DIR_SOUTH, PlayerState.USER, "TO CHANGE")
    canvas.data["Player_02"] = Player(Orientation.DIR_NORTH, PlayerState.AI, "NoRTH")
    canvas.data["Player_03"] = Player(Orientation.DIR_EAST, PlayerState.AI, "eaST")
    canvas.data["Player_04"] = Player(Orientation.DIR_WEST, PlayerState.AI, "WeST")

    canvas.data["splashTextField"] = TextField(X_CENTER, Y_LOC_TOP_BUTTON, "Type name...", L_TEXT_SIZE)
    canvas.data["level"] = Level()

### run - run the program
def runUI() :
    # initialize canvas
    root = Tk()
    canvas = Canvas(root, width=CANVAS_WIDTH, height= CANVAS_HEIGHT, background="white")
    canvas.pack()

    # make it so the window is not resizable
    root.resizable(height = 0, width = 0)

    # give the canvas a title
    root.title("Multegula")

    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas

    # set up dicitonary
    canvas.data = {}

    # sets up events
    #root.bind("<Key>", keyPressed)
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    root.bind("<KeyRelease>", keyReleased)

    # let the games begin
    init(canvas)
    redrawAll(canvas)
    root.mainloop()