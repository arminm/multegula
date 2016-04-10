# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# Paddle.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
from enum import Enum
import random
from UI.typedefs import *
from bridges.GoBridge import PyMessage

# PADDLE class
class Paddle :
    ### __init__ - initialize and return a paddle
    ##  @param orientation - location on the screen of this padde (DIR_NORTH/DIR_SOUTH/...)
    ##  @param state - current control state of the player (USER/AI/COMP)
    def __init__(self, orientation, state, gameType) :
        # CONSTANT fields   
        self.ORIENTATION = orientation
        self.COLORS = ['red', 'green', 'blue', 'purple', 'orange', 'yellow', 'black', 'white']

        # dynamic fields
        self.state = state
        self.speed = PADDLE_SPEED_INIT 
        self.direction = Direction.DIR_STOP
        self.center = X_CENTER
        self.width = PADDLE_WIDTH_INIT
        self.color = 'black'
        self.randomColor()
        self.redraw = False
        self.first = True
        self.gameType = gameType;

    ### increase/decrease speed methods
    def increaseSpeed(self) :
        self.speed *= 1.1

    def decreaseSpeed(self) :
        self.speed *= 0.9

    ### increase/decrease width methods
    def increaseWidth(self) :
        self.width *= 1.1
        self.redraw = True

    def decreaseWidth(self) :
        self.width -= 0.9
        self.redraw = True

    ### get/set COLOR methods
    def randomColor(self) :
        currentColor = self.color
        newColor = currentColor

        # loop until a new color has been chosen
        while (currentColor == newColor) :
            newColor = random.choice(self.COLORS)

        # set new color
        self.color = newColor
        self.redraw = True

    def setColor(self, color) :
        self.color = color
        self.redraw = True

    ### move - move the paddle based on the current direction
    def move(self) :
        # move paddle left if not already at the MIN possible
        if((self.direction == Direction.DIR_LEFT) and ((self.center - self.width) > PADDLE_MIN)) :
            self.center = self.center - self.speed
            self.redraw = True
        # move paddle right if not already at the MAX possible
        elif((self.direction == Direction.DIR_RIGHT) and ((self.center + self.width) < PADDLE_MAX)) :
            self.center = self.center + self.speed
            self.redraw = True
        else :
            self.redraw = False

    def setPaddle(self, canvas) :
        (leftEdge, rightEdge, topEdge, bottomEdge) = self.getEdges()
        self.p = canvas.create_rectangle(leftEdge, topEdge, rightEdge, bottomEdge,
                                            fill = self.color, width = BORDER_WIDTH)
    ### draw - draw the paddle
    def draw(self, canvas) : 
        # if this is not the first draw and there has been an update
        if(not(self.first) and self.redraw) :
            canvas.delete(self.p)
            self.setPaddle(canvas)
            self.redraw = False

            # if this is a multi-player game send an update
            if self.gameType == GameType.MULTI_PLAYER:
                print('sending an update');
                toSend = PyMessage()
                toSend.src = canvas.data['myName']
                toSend.kind = 'MSG_PADDLE'
                toSend.content = str(self.center) + '|' + str(self.width)
                toSend.multicast = True
                canvas.data['bridge'].sendMessage(toSend)

        # if this is the first time
        elif(self.first) :
            self.setPaddle(canvas)
            self.first = False

            # if this is a multi-player game send an update
            if self.gameType == GameType.MULTI_PLAYER:
                print('UI: sending an update');
                toSend = PyMessage()
                toSend.src = canvas.data['myName']
                toSend.kind = 'MSG_PADDLE'
                toSend.content = str(self.center) + '|' + str(self.width)
                toSend.multicast = True
                canvas.data['bridge'].sendMessage(toSend)

    ### update - update the paddle location (that is, 'move' if applicable) and draw
    def update(self, canvas) :
        state = self.state

        if((state == PlayerState.USER) or (state == PlayerState.AI)) :
            self.move()
            self.draw(canvas)
        elif(state == PlayerState.COMP) :
            self.draw(canvas)

    ### getInfo - get pertinent information about the paddle
    def getInfo(self) :
        return (self.center, self.width, self.direction, self.ORIENTATION)

    ### getEdges - get the edges of the paddle based on the orientation
    def getEdges(self) :
        center = self.center
        width = self.width
        
        # edges of the NORTH paddle
        if(self.ORIENTATION == Orientation.DIR_NORTH) :
            leftEdge    = center - width
            rightEdge   = center + width
            topEdge     = PADDLE_MARGIN
            bottomEdge  = PADDLE_MARGIN + PADDLE_HEIGHT     

        # edges of the SOUTH paddle
        elif(self.ORIENTATION == Orientation.DIR_SOUTH) :
            leftEdge    = center - width
            rightEdge   = center + width
            topEdge     = CANVAS_HEIGHT - PADDLE_HEIGHT - PADDLE_MARGIN
            bottomEdge  = CANVAS_HEIGHT - PADDLE_MARGIN

        # edges of the EAST paddle
        elif(self.ORIENTATION == Orientation.DIR_EAST) :
            leftEdge    = CANVAS_WIDTH - PADDLE_MARGIN - PADDLE_HEIGHT
            rightEdge   = CANVAS_WIDTH - PADDLE_MARGIN
            topEdge     = center - width
            bottomEdge  = center + width 

        # edges of the WEST paddle
        elif(self.ORIENTATION == Orientation.DIR_WEST) :
            leftEdge    = PADDLE_MARGIN
            rightEdge   = PADDLE_MARGIN + PADDLE_HEIGHT
            topEdge     = center - width
            bottomEdge  = center + width

        # left right top 
        return (leftEdge, rightEdge, topEdge, bottomEdge)




