# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# MenuScreen.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

from components.ComponentDefs import *

# Menu Screen - buttons will be superimpsed on top of this screen to allow the user to
#   either start a solo game or join a network game.
class MenuScreen :
    ### __init__ - initialize and return a MenuScreen
    def __init__(self) :
        self.firstBack = True
        self.firstText = True

    def setBackground(self, canvas) :
        self.background = canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill = "black", width = 0)

        self.foreground = canvas.create_rectangle(X_MARGIN, Y_MARGIN, CANVAS_WIDTH - X_MARGIN,
                                                    CANVAS_HEIGHT - Y_MARGIN, fill = "white", width = 0)

    def setText(self, canvas) :
        self.title  = canvas.create_text(X_CENTER, Y_LOC_TITLE, text = "MULTEGULA",
                                        font = ("Courier", XL_TEXT_SIZE))

        self.t1     = canvas.create_text(X_CENTER, Y_LOC_AUTHOR1, text = "created by",
                                        font = ("Courier", M_TEXT_SIZE))
        
        self.t2     = canvas.create_text(X_CENTER, Y_LOC_AUTHOR2, text = "DS Team Misfits",
                                        font = ("Courier", M_TEXT_SIZE))
    ### drawBackground - draw white background with a white border
    def drawBackground(self, canvas) :
        if(self.firstBack) :
            self.setBackground(canvas)
            self.firstBack = False

    ### drawText - place text over top of background
    def drawText(self, canvas) :
        if(not(self.firstText)) :
            canvas.delete(self.title)
            canvas.delete(self.t1)
            canvas.delete(self.t2)
            self.setText(canvas)
        else :
            self.setText(canvas)
            self.firstText = False

