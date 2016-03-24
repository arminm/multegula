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
from screens.MenuScreen import *
from screens.PausedScreen import *
from screens.Screens import *


def mousePressed(event):
    # initialize variables
    canvas = event.widget.canvas

    # if the splashscreen is up, call helper function
    if (canvas.data["currentScreen"] == Screens.SCRN_MAIN): 
        if(canvas.data["soloButton"].clicked(event.x, event.y)):
            canvas.data["currentScreen"] = Screens.SCRN_PAUSE;
            canvas.data["nextScreen"] = Screens.SCRN_GAME;
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
    canvas.data["menuScreen"] = MenuScreen(CANVAS_WIDTH, CANVAS_HEIGHT);
    canvas.data["pausedScreen"] = PausedScreen(CANVAS_WIDTH, CANVAS_HEIGHT);

    def timerFired():
        canvas.delete(ALL);

        # if the splash screen is up, make sure tha splash screen is called
        if(canvas.data["currentScreen"] == Screens.SCRN_MAIN):
            canvas.data["menuScreen"].drawBackground(canvas);
            canvas.data["ball"].moveAndDraw(canvas);
            canvas.data["menuScreen"].drawText(canvas);
            canvas.data["soloButton"].draw(canvas);
            canvas.data["joinButton"].draw(canvas);

        elif(canvas.data["currentScreen"] == Screens.SCRN_PAUSE):
            canvas.data["pausedScreen"].draw(canvas);

        canvas.after(canvas.data["delay"], timerFired);

    timerFired();


## INITIALIZES the dictionary: takes "canvas", returns None
## # this function uses local functions (for organization purposes) to
## # # initialize all of thevalues in the dictionary
def init(canvas):
    # current screen
    canvas.data["currentScreen"] = Screens.SCRN_MAIN;
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

    # let the games begin
    init(canvas)
    redrawAll(canvas)

    # This call BLOCKS (so your program waits until you close the window!)
    root.mainloop()

run()
