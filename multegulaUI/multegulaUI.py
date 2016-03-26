# EXAMPLE UI CODE FROM BLOCKBUSTER
# For porting to Multegula
# Adapted for Python 3 by Garrett Miller and 2to3 utility
#
# by daniel santoro. ddsantor.

##### IMPORT MODULES #####
from tkinter import *
import random
from components.Ball import *
from components.Button import *
from components.Paddle import *
from components.ComponentDefs import *
from screens.SplashScreen import *
from screens.MenuScreen import *
from screens.PauseScreen import *
from screens.ScreenEnum import *
from screens.GameScreen import *

def keyPressed(event):
    # initialize variable
    canvas = event.widget.canvas;
    currentScreen = canvas.data["currentScreen"];

    if(currentScreen == Screens.SCRN_SPLASH):
        tempName = canvas.data["playerName"];

        # add new characters
        if(("!" <= event.char <= "z") and (len(tempName) <= 16)):
            # initial name - clear it
            if(tempName == "Type name..."):
                tempName = "";
            tempName += event.char;
        elif(event.keysym == "BackSpace"):
            # initial name - clear it
            if(tempName == "Type name..."):
                tempName = "";
            else:
                tempName = tempName[:-1];
        elif((event.keysym == "space") and (len(tempName) <= 16)):
            # initial name - clear it
            if(tempName == "Type name..."):
                tempName = "";
            else:
                tempName += " ";
        elif((event.keysym == "Return") and (tempName != "Type name...")):
            canvas.data["currentScreen"] = Screens.SCRN_MAIN;

        # set name
        canvas.data["playerName"] = tempName;

    elif((currentScreen == Screens.SCRN_PAUSE) or (currentScreen == Screens.SCRN_GAME)):
        if((event.keysym == "Left") or (event.keysym == "a") or (event.keysym == "A")):
            canvas.data["paddle_01"].setDirection(Direction.DIR_LEFT);
        elif((event.keysym == "Right") or (event.keysym == "d") or (event.keysym == "D")):
            canvas.data["paddle_01"].setDirection(Direction.DIR_RIGHT);

def keyReleased(event):
    canvas = event.widget.canvas;
    currentScreen = canvas.data["currentScreen"];

    if((currentScreen == Screens.SCRN_PAUSE) or (currentScreen == Screens.SCRN_GAME)):
        if((event.keysym == "Left") or (event.keysym == "a") or (event.keysym == "A") or 
            (event.keysym == "Right") or (event.keysym == "d") or (event.keysym == "D")):
            canvas.data["paddle_01"].setDirection(Direction.DIR_STOP);

def mousePressed(event):
    # initialize variables
    canvas = event.widget.canvas;

    # if the splashscreen is up, call helper function
    if (canvas.data["currentScreen"] == Screens.SCRN_MAIN): 
        if(canvas.data["soloButton"].clicked(event.x, event.y)):
            canvas.data["currentScreen"] = Screens.SCRN_PAUSE;
            canvas.data["nextScreen"] = Screens.SCRN_GAME;
            canvas.data["ball"].reset();
        elif(canvas.data["joinButton"].clicked(event.x, event.y)):
            print("JOIN");

## REDRAW all: takes "canvas", returns None
## # this function draws everything on the canvas with A LOT of help
## # # from helper functions. It makes sure the correct functions are
## # # # called.        
def redrawAll(canvas):    
    # EXTRACT information from the canvas
    # # canvas variables
    CANVAS_HEIGHT = canvas.data["CANVAS_HEIGHT"]
    CANVAS_WIDTH = canvas.data["CANVAS_WIDTH"]

    Y_LOC_TOP_BUTTON    = canvas.data["Y_LOC_TOP_BUTTON"];
    Y_LOC_BOTTOM_BUTTON = canvas.data["Y_LOC_BOTTOM_BUTTON"];

    # # text sizes
    S_TEXT_SIZE   = canvas.data["S_TEXT_SIZE"];
    M_TEXT_SIZE   = canvas.data["M_TEXT_SIZE"];
    L_TEXT_SIZE   = canvas.data["L_TEXT_SIZE"];
    XL_TEXT_SIZE  = canvas.data["XL_TEXT_SIZE"];

    # general location variables
    X_CENTER  = CANVAS_WIDTH // 2;
    Y_CENTER  = CANVAS_HEIGHT // 2;
    X_MARGIN  = CANVAS_WIDTH // 30;
    Y_MARGIN  = CANVAS_HEIGHT // 30;

    canvas.data["soloButton"] = Button(CANVAS_WIDTH, CANVAS_HEIGHT, X_CENTER, Y_LOC_TOP_BUTTON, "Solo Game", True);
    canvas.data["joinButton"] = Button(CANVAS_WIDTH, CANVAS_HEIGHT, X_CENTER, Y_LOC_BOTTOM_BUTTON, "Join Game", False);
    canvas.data["ball"] = Ball(CANVAS_WIDTH, CANVAS_HEIGHT);
    canvas.data["splashScreen"] = SplashScreen(CANVAS_WIDTH, CANVAS_HEIGHT);
    canvas.data["menuScreen"] = MenuScreen(CANVAS_WIDTH, CANVAS_HEIGHT);
    canvas.data["pauseScreen"] = PauseScreen(CANVAS_WIDTH, CANVAS_HEIGHT);
    canvas.data["gameScreen"] = GameScreen(CANVAS_WIDTH, CANVAS_HEIGHT);
    canvas.data["paddle_01"] = Paddle(CANVAS_WIDTH, CANVAS_HEIGHT, Orientation.DIR_SOUTH, PaddleState.USER);
    canvas.data["paddle_02"] = Paddle(CANVAS_WIDTH, CANVAS_HEIGHT, Orientation.DIR_NORTH, PaddleState.AI);
    canvas.data["paddle_03"] = Paddle(CANVAS_WIDTH, CANVAS_HEIGHT, Orientation.DIR_EAST, PaddleState.AI);
    canvas.data["paddle_04"] = Paddle(CANVAS_WIDTH, CANVAS_HEIGHT, Orientation.DIR_WEST, PaddleState.AI);

    def timerFired():
        canvas.delete(ALL);

        # if the splash screen is up, make sure tha splash screen is called
        if(canvas.data["currentScreen"] == Screens.SCRN_SPLASH):
            canvas.data["splashScreen"].drawBackground(canvas);
            canvas.data["ball"].updateSplash(canvas);
            canvas.data["splashScreen"].drawText(canvas);
            if(canvas.data["playerName"] == "Type name..."):
                canvas.create_text(X_CENTER, Y_LOC_TOP_BUTTON, 
                    text = canvas.data["playerName"], 
                    font = ("Courier", L_TEXT_SIZE), fill = "grey"); 
            else:
                canvas.create_text(X_CENTER, Y_LOC_TOP_BUTTON, 
                    text = canvas.data["playerName"], 
                    font = ("Courier", L_TEXT_SIZE), fill = "black");             


        elif(canvas.data["currentScreen"] == Screens.SCRN_MAIN):
            canvas.data["menuScreen"].drawBackground(canvas);
            canvas.data["ball"].updateSplash(canvas);
            canvas.data["menuScreen"].drawText(canvas);
            canvas.data["soloButton"].draw(canvas);
            canvas.data["joinButton"].draw(canvas);

        elif(canvas.data["currentScreen"] == Screens.SCRN_PAUSE):
            canvas.data["gameScreen"].drawBackground(canvas);
            canvas.data["ball"].draw(canvas);
            canvas.data["paddle_01"].update(canvas);
            canvas.data["paddle_02"].update(canvas);
            canvas.data["paddle_03"].update(canvas);
            canvas.data["paddle_04"].update(canvas);
            canvas.data["pauseScreen"].draw(canvas);

        elif(canvas.data["currentScreen"] == Screens.SCRN_GAME):
            canvas.data["gameScreen"].drawBackground(canvas);
            canvas.data["ball"].updateGame(canvas);
            canvas.data["paddle_01"].update(canvas);
            canvas.data["paddle_02"].update(canvas);
            canvas.data["paddle_03"].update(canvas);
            canvas.data["paddle_04"].update(canvas);

        canvas.after(canvas.data["delay"], timerFired);

    timerFired();


## INITIALIZES the dictionary: takes "canvas", returns None
## # this function uses local functions (for organization purposes) to
## # # initialize all of thevalues in the dictionary
def init(canvas):
    # current screen
    canvas.data["currentScreen"] = Screens.SCRN_SPLASH;
    canvas.data["nextScreen"] = Screens.SCRN_NONE;

    canvas.data["Y_LOC_TOP_BUTTON"]     = 0.70*canvas.data["CANVAS_HEIGHT"];
    canvas.data["Y_LOC_BOTTOM_BUTTON"]  = 0.85*canvas.data["CANVAS_HEIGHT"];

    # misc
    canvas.data["delay"] = 10;

    # text
    canvas.data["S_TEXT_SIZE"] = canvas.data["CANVAS_WIDTH"] // 35
    canvas.data["M_TEXT_SIZE"] = canvas.data["CANVAS_WIDTH"] // 28
    canvas.data["L_TEXT_SIZE"] = canvas.data["CANVAS_WIDTH"] // 20
    canvas.data["XL_TEXT_SIZE"] = canvas.data["CANVAS_WIDTH"] // 10

    canvas.data["currentTextLevel"] = "LEVEL ONE.";

    canvas.data["playerName"] = "Type name...";

## RUN the program
## # this function starts the program running
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

    # store values in the dictionary that will not need to be reset
    # # when most else needs to be.  These variables will be changed
    # # # in the code as needed
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

    # This call BLOCKS (so your program waits until you close the window!)
    root.mainloop()

run()
