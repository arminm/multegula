 # 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# Ball.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
import random
from enum import Enum
from UI.typedefs import *

# BALL class
class Ball :
    ### __init___ - initialize and return ball
    def __init__(self) :
        # constant fields
        self.COLORS = ['red', 'green', 'blue', 'purple', 'orange', 'yellow']

        # dynamic fields
        self.xCenter = CANVAS_WIDTH // 2
        self.yCenter = CANVAS_HEIGHT // 2
        self.radius = CANVAS_WIDTH // 50
        self.color = 'green'
        self.xVelocity = 0
        self.yVelocity = CANVAS_WIDTH // 110
        self.first = True
        self.lastToTouch = ''

    ### reset - reset dynamic ball location/speed properties 
    def reset(self) :
        self.randomXVelocity()
        self.yVelocity = random.choice([-1, 1])*CANVAS_WIDTH // 110
        self.xCenter = CANVAS_WIDTH // 2
        self.yCenter = CANVAS_HEIGHT // 2
        self.randomColor()
        self.lastToTouch = '';

    ### getEdges - get the edges of the ball
    def getEdges(self) :
        x = self.xCenter
        y = self.yCenter
        r = self.radius

        # left, right, top, bottom
        return (x - r, x + r, y - r, y + r)

    ### get/set CENTER methods
    def setCenter(self, xCenter, yCenter) :
        self.xCenter = xCenter
        self.yCenter = yCenter

    def getCenter(self) :
        return(self.xCenter, self.yCenter)

    ### get/set RADIUS methods
    def increaseRadius(self) :
        self.radius *= 1.1

    def decreaseRadius(self) :
        self.radius *= 0.9

    ### get/set VELOCITY methods
    def setVelocity(self, xVelocity, yVelocity) :
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity

    def increaseVelocity(self) :
        self.xVelocity *= 1.1
        self.yVelocity *= 1.1

    def decreaseVelocity(self) :
        self.xVelocity *= 0.9
        self.yVelocity *= 0.9

    def randomXVelocity(self) :
        speed = CANVAS_WIDTH // 110
        factor = random.random()
        factor *= random.randint(-2, 2)
        self.xVelocity = speed*factor

    def randomYVelocity(self) :
        speed = CANVAS_WIDTH // 110
        factor = random.random()
        factor *= random.randint(-2, 2)
        self.yVelocity = speed*factor  

    def getVelocity(self) :
        return (self.xVelocity, self.yVelocity) 

    ### get/set COLOR methods
    def randomColor(self) :
        currentColor = self.color
        newColor = currentColor

        # loop until a new color has been chosen
        while (currentColor == newColor) :
            newColor = random.choice(self.COLORS)

        # set new color
        self.color = newColor     

    ### moveMenu - 
    ##  The method moves the ball around the screen and bounces it off of walls. This mode
    ##  is meant for use on menu screens only.
    def moveMenu(self) :
        # dynamic variables
        xCenter = self.xCenter
        yCenter = self.yCenter
        radius = self.radius
        xVelocity = self.xVelocity
        yVelocity = self.yVelocity

        # UPDATE Y VELOCITY - 
        # Bounce ball off of bottom wall...
        if ((yCenter + radius) >= CANVAS_HEIGHT) and (yVelocity > 0) :
            self.randomXVelocity()
            self.randomColor()
            self.yVelocity -= (2*yVelocity)
        # Bounce ball off of top wall...
        elif ((yCenter - radius) <= 0) and (yVelocity < 0) :
            self.randomColor()
            self.yVelocity -= (2*yVelocity)
        # Move the ball
        else : 
            self.yCenter += yVelocity

        # UPDATE X VELOCITY -
        # Bounce ball off left wall
        if ((xCenter - radius) <= 0) and (xVelocity < 0) :
            self.randomColor()
            self.xVelocity -= (xVelocity*2)
        # Bounce ball off right wall
        elif ((xCenter + radius) >= CANVAS_WIDTH) and (xVelocity > 0) :
            self.randomColor()
            self.xVelocity -= (xVelocity*2)
        # Move ball
        else : 
            self.xCenter += xVelocity 

    ### moveGame - move the ball during gameplay.
    def moveGame(self) :
        self.xCenter += self.xVelocity 
        self.yCenter += self.yVelocity 


    ### setBall - set the ball in the canvas
    def setBall(self, canvas) : 
        color   = self.color
        xCenter = self.xCenter
        yCenter = self.yCenter
        radius  = self.radius

        self.ball = canvas.create_oval(xCenter - radius,
                                        yCenter - radius,
                                        xCenter + radius,
                                        yCenter + radius,
                                        fill = color, width = BORDER_WIDTH)
        
    ### draw - handles the drawing of the bills 
    def draw(self, canvas) :
        if not(self.first) :
            canvas.delete(self.ball)
            self.setBall(canvas)
        else :
            self.setBall(canvas)
            self.first = False

    ### updateMenu - general purpose menu update function
    def updateMenu(self, canvas) : 
        self.moveMenu() 
        self.draw(canvas)

    ### updateGame - general purpose game update function
    def updateGame(self, canvas) :
        self.moveGame()
        self.draw(canvas)

    ### getInfo - get ball info
    def getInfo(self) : 
        return(self.xCenter, self.yCenter, self.radius)


