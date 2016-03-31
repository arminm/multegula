# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# Paddle.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
from enum import Enum
from components.ComponentDefs import *

#
class Block :
    def __init__(self, canvas_width, canvas_height, xCenter, yCenter, initPwr, tilt) :
        self.CANVAS_WIDTH = canvas_width
        self.CANVAS_HEIGHT = canvas_height
        self.X_CENTER = xCenter
        self.Y_CENTER = yCenter
        self.powerUp = initPwr
        self.WIDTH = canvas_width // 10
        self.HEIGHT = canvas_height // 50
        self.BORDER_WIDTH = canvas_width // 350
        self.TILT = tilt
        self.enabled = True
        self.first = True
        self.changed = False

    def enable(self) :
        if self.enabled == False :
            self.enabled = True
            self.changed = True

    def disable(self) :
        if self.enabled == True :
            self.enabled = False
            self.changed = True

    def setBlock(self, canvas) :
        (leftEdge, rightEdge, topEdge, bottomEdge) = self.getEdges()

        color = "white"
        self.b = canvas.create_rectangle(leftEdge, topEdge, rightEdge, bottomEdge,
                                            fill = color, width = self.BORDER_WIDTH)  
        
    ### draw - draw the block
    def draw(self, canvas) : 
        if not(self.first) and self.changed :
            canvas.delete(self.b)
            if(self.enabled) :
                self.setBlock(canvas)
            self.changed = False
        elif self.first :
            self.setBlock(canvas)
            self.first = False


        ### getEdges - get the edges of the paddle based on the orientation
    def getEdges(self) :
        HEIGHT = self.HEIGHT
        WIDTH = self.WIDTH
        X_CENTER = self.X_CENTER
        Y_CENTER = self.Y_CENTER

        # vertical paddle
        if self.TILT == Tilt.HORZ :
            leftEdge    = X_CENTER - WIDTH
            rightEdge   = X_CENTER + WIDTH
            topEdge     = Y_CENTER - HEIGHT
            bottomEdge  = Y_CENTER + HEIGHT     

        # edges of the SOUTH paddle
        elif self.TILT == Tilt.VERT :
            leftEdge    = X_CENTER - HEIGHT
            rightEdge   = X_CENTER + HEIGHT
            topEdge     = Y_CENTER - WIDTH
            bottomEdge  = Y_CENTER + WIDTH

        return (leftEdge, rightEdge, topEdge, bottomEdge) 
