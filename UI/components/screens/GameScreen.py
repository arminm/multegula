# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# GameScreen.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
from UI.typedefs import *

# GameScreen - the paddles, ball, bricks, an status info will be superimposed on this
#   screen during gameplay.
class GameScreen :
    ### __init__ - initialize and return a GameScreen
    def __init__(self) :
        self.first = True

    ### set - sets the screen in the canvas
    def set(self, canvas) :
        self.background = canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill = 'black', width = 0)

        self.foreground = canvas.create_rectangle(X_MARGIN, Y_MARGIN, CANVAS_WIDTH - X_MARGIN,
                                                    CANVAS_HEIGHT - Y_MARGIN, fill = 'white', width = 0)
    ### draw - manages drawing the screen
    def draw(self, canvas) :
        if(self.first) :
            self.set(canvas)
            self.first = False

