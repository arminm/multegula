# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# SplashScreen.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
from components.ComponentDefs import *

# SplashScreen - first thing visible to a user. A name prompt is to be superimposed
#   over top of this class.
class SplashScreen :
    ### __init__ - initialize and return a MenuScreen
    def __init__(self) :
        self.firstBack = True
        self.firstText = True

    ### setBackground - set the background in the canvsa
    def setBackground(self, canvas) :
        # draw text
        self.background = canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill = "black", width = 0)
        self.foreground = canvas.create_rectangle(X_MARGIN, Y_MARGIN, CANVAS_WIDTH - X_MARGIN,
                                                    CANVAS_HEIGHT - Y_MARGIN, fill = "white", width = 0)  

    ### setText - set the text in the canvas
    def setText(self, canvas) :
        # draw text
        self.title = canvas.create_text(X_CENTER, Y_LOC_TITLE, text = "MULTEGULA",
                                        font = ("Courier", XL_TEXT_SIZE))
        self.prompt = canvas.create_text(X_CENTER, Y_LOC_PROMPT, text = "Welcome. Tell us your name...",
                                            font = ("Courier", M_TEXT_SIZE))    

    ### drawBackground - manages drawing of the background
    def drawBackground(self, canvas) :
        if(self.firstBack) :
            self.setBackground(canvas)
            self.firstBack = False

    ### drawText - manages drawing of the text
    def drawText(self, canvas) :
        if(not(self.firstText)) :
            canvas.delete(self.title)
            canvas.delete(self.prompt)
            self.setText(canvas)
        else :
            self.setText(canvas)
            self.firstText = False


