# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# Button.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
from UI.typedefs import *

# GAMEOVER class
class GameOver :
    ### __init__ - initialize and return a GameScreen
    def __init__(self) :
        self.first = True

    ### set - set the background in the canvas
    def set(self, canvas) :
        self.background = canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill = 'black', width = 0)

        self.foreground = canvas.create_rectangle(X_MARGIN, Y_MARGIN, CANVAS_WIDTH - X_MARGIN,
                                                    CANVAS_HEIGHT - Y_MARGIN, fill = 'white', width = 0)

        self.title  = canvas.create_text(X_CENTER, Y_LOC_TITLE, text = 'MULTEGULA',
                                        font = ('Courier', XL_TEXT_SIZE))

        self.title  = canvas.create_text(X_CENTER, Y_CENTER, text = 'GAME OVER.',
                                        font = ('Courier', L_TEXT_SIZE))

    ### draw -  manages the drawing of the background
    def draw(self, canvas) :
        if(self.first) :
            self.set(canvas)
            self.first = False