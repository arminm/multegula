# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# Block.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
from enum import Enum
from UI.typedefs import *
import random

# BLOCK class
class Block :
    ### __init__ - initialize and return block
    ##  @param xCenter - x-coordinate for the center of the button
    ##  @param yButton - y-coordinate for the center of the button
    ##  @param initPwr - initial power up state of the block
    ##  @param tilt - the orientation of the block (vert/horz)
    def __init__(self, xCenter, yCenter, initPwr, tilt) :
        self.X_CENTER = xCenter
        self.Y_CENTER = yCenter
        self.powerUp = initPwr
        self.TILT = tilt
        self.enabled = True
        self.first = True
        self.changed = False
        self.COLORS = ['red', 'green', 'blue', 'purple', 'orange', 'yellow', 'white']

    ### translate - translate the position and tilt based on oriention
    def translate(self, levelOrientation) :
        ## SOUTH -> nothing changes
        if levelOrientation == Orientation.DIR_SOUTH :
            return (self.X_CENTER, self.Y_CENTER, self.TILT)

        ## EAST -> translate position and tilt
        elif levelOrientation == Orientation.DIR_EAST :
            if self.TILT == Tilt.HORZ :
                return (CANVAS_WIDTH - self.Y_CENTER, self.X_CENTER, Tilt.VERT)
            elif self.TILT == Tilt.VERT :
                return (CANVAS_WIDTH - self.Y_CENTER, self.X_CENTER, Tilt.HORZ)

        ## NORTH -> translate position
        elif levelOrientation == Orientation.DIR_NORTH :
            return (CANVAS_WIDTH - self.X_CENTER, CANVAS_HEIGHT - self.Y_CENTER, self.TILT)

        ## WEST -> translate position and tilt
        elif levelOrientation == Orientation.DIR_WEST :
            if self.TILT == Tilt.HORZ:
                return (self.Y_CENTER, CANVAS_HEIGHT - self.X_CENTER, Tilt.VERT)
            elif self.TILT == Tilt.VERT : 
                return (self.Y_CENTER, CANVAS_HEIGHT - self.X_CENTER, Tilt.HORZ)

    ### getEdges - get the edges of the block based on the orientation
    def getEdges(self, levelOrientation) :
        (xCenter, yCenter, tilt) = self.translate(levelOrientation) 

        # horizontal block
        if tilt == Tilt.HORZ :
            leftEdge    = xCenter - BLOCK_WIDTH
            rightEdge   = xCenter + BLOCK_WIDTH
            topEdge     = yCenter - BLOCK_HEIGHT
            bottomEdge  = yCenter + BLOCK_HEIGHT     

        # vertical paddle
        elif tilt == Tilt.VERT :
            leftEdge    = xCenter - BLOCK_HEIGHT
            rightEdge   = xCenter + BLOCK_HEIGHT
            topEdge     = yCenter - BLOCK_WIDTH
            bottomEdge  = yCenter + BLOCK_WIDTH

        return (leftEdge, rightEdge, topEdge, bottomEdge) 

    ### enable - enable the use of this block if appropriate
    def enable(self) :
        if self.enabled == False :
            self.enabled = True
            self.changed = True

    ### disable - disable the use of this block if appropriate
    def disable(self) :
        if self.enabled == True :
            self.enabled = False
            self.changed = True

    ### setBlock - set the block in the canvas
    def setBlock(self, canvas, levelOrientation) :
        (leftEdge, rightEdge, topEdge, bottomEdge) = self.getEdges(levelOrientation)

        ## TODO: THE COLOR SHOULD BE SET BASED ON THE POWER UP
        ## But for now, we're just going to set it to a random value.
        color = random.choice(self.COLORS)

        self.b = canvas.create_rectangle(leftEdge, topEdge, rightEdge, bottomEdge,
                                            fill = color, width = BORDER_WIDTH)  
        
    ### draw - draw the block
    def draw(self, canvas, levelOrientation) : 
        if not(self.first) and self.changed :
            canvas.delete(self.b)
            if(self.enabled) :
                self.setBlock(canvas, levelOrientation)
            self.changed = False
        elif self.first :
            self.setBlock(canvas, levelOrientation)
            self.first = False
