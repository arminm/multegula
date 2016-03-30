# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# multegulaUI.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

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
from screens.GameScreen import *

from levels.Level01 import *

### keyPressed - handle keypressed events
def keyPressed(event):
    canvas = event.widget.canvas
    currentScreen = canvas.data["currentScreen"]

    # handle splash screen events - entering a name
    if(currentScreen == Screens.SCRN_SPLASH):
        # add new characters
        if("!" <= event.char <= "z"):
            canvas.data["splashTextField"].addChar(event.char)            
        # remove characters
        elif(event.keysym == "BackSpace"):
            canvas.data["splashTextField"].deleteChar()            
        # addd space 
        elif(event.keysym == "space"):
            canvas.data["splashTextField"].addChar(" ")            
        # enter the name
        elif((event.keysym == "Return") and canvas.data["splashTextField"].getChanged()):
            canvas.data["currentScreen"] = Screens.SCRN_MENU

        # set name
        canvas.data["playerName"] = canvas.data["splashTextField"].getText()

    # pause screen / gameplay keyPressed events - move the paddle
    elif((currentScreen == Screens.SCRN_PAUSE) or (currentScreen == Screens.SCRN_GAME)):
        if((event.keysym == "Left") or (event.keysym == "a") or (event.keysym == "A")):
            canvas.data["Player_01"].setDirection(Direction.DIR_LEFT)
        elif((event.keysym == "Right") or (event.keysym == "d") or (event.keysym == "D")):
            canvas.data["Player_01"].setDirection(Direction.DIR_RIGHT)

### keyReleased - handle key release events
def keyReleased(event):
    canvas = event.widget.canvas
    currentScreen = canvas.data["currentScreen"]

    # pause screen / gameplay keyReleased events - stop paddle motion
    if((currentScreen == Screens.SCRN_PAUSE) or (currentScreen == Screens.SCRN_GAME)):
        if((event.keysym == "Left") or (event.keysym == "a") or (event.keysym == "A") or 
            (event.keysym == "Right") or (event.keysym == "d") or (event.keysym == "D")):
            canvas.data["Player_01"].setDirection(Direction.DIR_STOP)

### mousePressed - handle mouse press events
def mousePressed(event):
    canvas = event.widget.canvas

    # main screen mouse pressed events - button clicks
    if (canvas.data["currentScreen"] == Screens.SCRN_MENU): 
        if(canvas.data["soloButton"].clicked(event.x, event.y)):
            canvas.data["currentScreen"] = Screens.SCRN_PAUSE
            canvas.data["nextScreen"] = Screens.SCRN_GAME
            canvas.data["ball"].reset()
            canvas.delete(ALL)
        elif(canvas.data["joinButton"].clicked(event.x, event.y)):
            print("JOIN")

### redrawAll - draw the game screen
def redrawAll(canvas):
    Y_LOC_TOP_BUTTON = canvas.data["Y_LOC_TOP_BUTTON"]
    X_CENTER  = canvas.data["CANVAS_WIDTH"] // 2
    L_TEXT_SIZE   = canvas.data["L_TEXT_SIZE"]

    ### SPLASH SCREEN
    if(canvas.data["currentScreen"] == Screens.SCRN_SPLASH):
        canvas.data["splashScreen"].drawBackground(canvas)
        canvas.data["ball"].updateMenu(canvas)
        canvas.data["splashScreen"].drawText(canvas)
        canvas.data["splashTextField"].draw(canvas)        

    ### MAIN SCREEN 
    elif(canvas.data["currentScreen"] == Screens.SCRN_MENU):
        canvas.data["menuScreen"].drawBackground(canvas)
        canvas.data["ball"].updateMenu(canvas)
        canvas.data["menuScreen"].drawText(canvas)
        canvas.data["soloButton"].draw(canvas)
        canvas.data["joinButton"].draw(canvas)

    ### PAUSE SCREEN
    elif(canvas.data["currentScreen"] == Screens.SCRN_PAUSE):
        canvas.data["gameScreen"].drawBackground(canvas)
        canvas.data["ball"].draw(canvas)
        canvas.data["Player_01"].update(canvas)
        canvas.data["Player_02"].update(canvas)
        canvas.data["Player_03"].update(canvas)
        canvas.data["Player_04"].update(canvas)
        canvas.data["pauseScreen"].draw(canvas)

    ### GAME SCREEN
    elif(canvas.data["currentScreen"] == Screens.SCRN_GAME):
        pass
        canvas.data["gameScreen"].drawBackground(canvas)
        canvas.data["Player_01"].update(canvas)
        canvas.data["Player_02"].update(canvas)
        canvas.data["Player_03"].update(canvas)
        canvas.data["Player_04"].update(canvas)
        canvas.data["level01"].update(canvas)
        canvas.data["ball"].updateGame(canvas)


    #  redraw after delay
    canvas.after(canvas.data["delay"], redrawAll, canvas)


### init - initialize dictionary
def init(canvas):
    # location constants
    CANVAS_HEIGHT = canvas.data["CANVAS_HEIGHT"]
    CANVAS_WIDTH = canvas.data["CANVAS_WIDTH"]
    canvas.data["Y_LOC_TOP_BUTTON"] = 0.70*CANVAS_HEIGHT
    canvas.data["Y_LOC_BOTTOM_BUTTON"] = 0.85*CANVAS_HEIGHT
    Y_LOC_TOP_BUTTON = canvas.data["Y_LOC_TOP_BUTTON"]
    Y_LOC_BOTTOM_BUTTON = canvas.data["Y_LOC_BOTTOM_BUTTON"]
    X_CENTER = CANVAS_WIDTH // 2
    Y_CENTER = CANVAS_HEIGHT // 2
    X_MARGIN = CANVAS_WIDTH // 30
    Y_MARGIN = CANVAS_HEIGHT // 30

    # current screen
    canvas.data["currentScreen"] = Screens.SCRN_SPLASH
    canvas.data["nextScreen"] = Screens.SCRN_NONE

    # text size
    canvas.data["S_TEXT_SIZE"] = canvas.data["CANVAS_WIDTH"] // 35
    canvas.data["M_TEXT_SIZE"] = canvas.data["CANVAS_WIDTH"] // 28
    canvas.data["L_TEXT_SIZE"] = canvas.data["CANVAS_WIDTH"] // 20
    canvas.data["XL_TEXT_SIZE"] = canvas.data["CANVAS_WIDTH"] // 10
    S_TEXT_SIZE = canvas.data["S_TEXT_SIZE"]
    M_TEXT_SIZE = canvas.data["M_TEXT_SIZE"]
    L_TEXT_SIZE = canvas.data["L_TEXT_SIZE"]
    XL_TEXT_SIZE = canvas.data["XL_TEXT_SIZE"]

    # misc
    canvas.data["delay"] = 10
    canvas.data["currentTextLevel"] = "LEVEL ONE."
    canvas.data["playerName"] = "Type name..."

    ### COMPONENETS
    # buttons
    canvas.data["soloButton"] = Button(CANVAS_WIDTH, CANVAS_HEIGHT, X_CENTER, Y_LOC_TOP_BUTTON, "Solo Game", True)
    canvas.data["joinButton"] = Button(CANVAS_WIDTH, CANVAS_HEIGHT, X_CENTER, Y_LOC_BOTTOM_BUTTON, "Join Game", False)

    # ball
    canvas.data["ball"] = Ball(CANVAS_WIDTH, CANVAS_HEIGHT)

    # screens
    canvas.data["gameScreen"]   = GameScreen(CANVAS_WIDTH, CANVAS_HEIGHT)
    canvas.data["menuScreen"]   = MenuScreen(CANVAS_WIDTH, CANVAS_HEIGHT)
    canvas.data["pauseScreen"]  = PauseScreen(CANVAS_WIDTH, CANVAS_HEIGHT)
    canvas.data["splashScreen"] = SplashScreen(CANVAS_WIDTH, CANVAS_HEIGHT)

    # players
    canvas.data["Player_01"] = Player(CANVAS_WIDTH, CANVAS_HEIGHT, Orientation.DIR_SOUTH, PlayerState.USER)
    canvas.data["Player_02"] = Player(CANVAS_WIDTH, CANVAS_HEIGHT, Orientation.DIR_NORTH, PlayerState.AI)
    canvas.data["Player_03"] = Player(CANVAS_WIDTH, CANVAS_HEIGHT, Orientation.DIR_EAST, PlayerState.AI)
    canvas.data["Player_04"] = Player(CANVAS_WIDTH, CANVAS_HEIGHT, Orientation.DIR_WEST, PlayerState.AI)

    canvas.data["splashTextField"] = TextField(X_CENTER, Y_LOC_TOP_BUTTON, "Type name...", L_TEXT_SIZE)
    canvas.data["level01"] = Level01(CANVAS_WIDTH, CANVAS_HEIGHT)

### run - run the program
def run():
    # intialize variables
    CANVAS_WIDTH = 700
    CANVAS_HEIGHT = CANVAS_WIDTH

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
    canvas.data["CANVAS_WIDTH"]  = CANVAS_WIDTH
    canvas.data["CANVAS_HEIGHT"] = CANVAS_HEIGHT

    # sets up events
    #root.bind("<Key>", keyPressed)
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    root.bind("<KeyRelease>", keyReleased)

    # let the games begin
    init(canvas)
    redrawAll(canvas)
    root.mainloop()

run()
