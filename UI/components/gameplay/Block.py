# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# Block.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
from enum import Enum
from UI.typedefs import *

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

    ### getEdges - get the edges of the block based on the orientation
    def getEdges(self) :
        # vertical paddle
        if self.TILT == Tilt.HORZ :
            leftEdge    = self.X_CENTER - BLOCK_WIDTH
            rightEdge   = self.X_CENTER + BLOCK_WIDTH
            topEdge     = self.Y_CENTER - BLOCK_HEIGHT
            bottomEdge  = self.Y_CENTER + BLOCK_HEIGHT     

        # edges of the SOUTH paddle
        elif self.TILT == Tilt.VERT :
            leftEdge    = self.X_CENTER - BLOCK_HEIGHT
            rightEdge   = self.X_CENTER + BLOCK_HEIGHT
            topEdge     = self.Y_CENTER - BLOCK_WIDTH
            bottomEdge  = self.Y_CENTER + BLOCK_WIDTH

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
    def setBlock(self, canvas) :
        (leftEdge, rightEdge, topEdge, bottomEdge) = self.getEdges()

        ## TODO: THE COLOR SHOULD BE SET BASED ON THE POWER UP
        color = 'white'

        self.b = canvas.create_rectangle(leftEdge, topEdge, rightEdge, bottomEdge,
                                            fill = color, width = BORDER_WIDTH)  
        
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
