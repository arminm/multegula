##### IMPORT MODULES #####
import random
from enum import Enum
from components.ComponentDefs import *

class Ball:
    def __init__(self, canvas_width, canvas_height):
        self.CANVAS_WIDTH = canvas_width;
        self.CANVAS_HEIGHT = canvas_height;
        self.BORDER_WIDTH = canvas_width // 350;
        self.COLORS = ["red", "green", "blue", "purple", "orange", "yellow"];

        self.color = "green";
        self.xVelocity = 0;
        self.yVelocity = canvas_width // 100;
        self.xCenter = canvas_width // 2;
        self.yCenter = canvas_height // 2;
        self.radius = canvas_width // 50;

    def reset(self):
        self.randomXVelocity();
        self.yVelocity = random.choice([-1, 1])*self.CANVAS_WIDTH // 100;
        self.xCenter = self.CANVAS_WIDTH // 2;
        self.yCenter = self.CANVAS_HEIGHT // 2;
        self.radius = self.CANVAS_WIDTH // 50;
        self.randomColor();

    # get/set center methods
    def setCenter(self, xCenter, yCenter):
        self.xCenter = xCenter;
        self.yCenter = yCenter;

    def getCenter(self):
        return(self.xCenter, self.yCenter);

    # get/set radius methods
    def setRadius(self, radius):
        self.radius = radius;

    def incrementRadius(self):
        self.radius *= 1.1;

    def decrementRadius(self):
        self.radius /= 0.9;

    def getRadius(self):
        return self.radius;

    # get/set speed methods
    def setSpeed(self, xVelocity, yVelocity):
        self.xVelocity = xVelocity;
        self.yVelocity = yVelocity;

    # get/set color methods
    def setColor(self, color):
        self.color = color;

    def randomColor(self):
        currentColor = self.color;
        newColor = currentColor;

        # loop until a new color has been chosen
        while (currentColor == newColor):
            newColor = random.choice(self.COLORS);

        # set new color
        self.color = newColor;

    def getColor(self):
        return self.color;

    # get/set speed methods
    def setVelocity(self, xVelocity, yVelocity):
        self.xVelocity = xVelocity;
        self.yVelocity = yVelocity;

    def randomXVelocity(self):
        speed = self.CANVAS_WIDTH // 100
        factor = random.random();
        factor *= random.randint(-2, 2);
        self.xVelocity = speed*factor;

    def randomYVelocity(self):
        speed = self.CANVAS_WIDTH // 100
        factor = random.random();
        factor *= random.randint(-2, 2);
        self.yVelocity = speed*factor;        

    def moveSplash(self):
        # these variables need to be called here because they are constantly changing
        xCenter = self.xCenter;
        yCenter = self.yCenter;
        xVelocity = self.xVelocity;
        yVelocity = self.yVelocity;
        radius = self.radius;
        CANVAS_WIDTH = self.CANVAS_WIDTH;
        CANVAS_HEIGHT = self.CANVAS_HEIGHT;

        # UPDATE Y VELOCITY - 
        if (((yCenter + radius) >= CANVAS_HEIGHT) and (yVelocity > 0)):
            self.randomXVelocity();
            self.randomColor();
            self.yVelocity -= (2*yVelocity);
        elif (((yCenter - radius) <= 0) and (yVelocity < 0)):
            self.randomColor();
            self.yVelocity -= (2*yVelocity);
        else: 
            self.yCenter += yVelocity

        # UPDATE X VELOCITY -
        if (((xCenter - radius) <= 0) and (xVelocity < 0)):
            self.randomColor();
            self.xVelocity -= (xVelocity*2);
        elif(((xCenter + radius) >= CANVAS_WIDTH) and (xVelocity > 0)):
            self.randomColor();
            self.xVelocity -= (xVelocity*2);
        else: 
            self.xCenter += xVelocity; 

    def moveGame(self):
        # these variables need to be called here because they are constantly changing
        xCenter = self.xCenter;
        yCenter = self.yCenter;
        xVelocity = self.xVelocity;
        yVelocity = self.yVelocity;
        radius = self.radius;
        CANVAS_WIDTH = self.CANVAS_WIDTH;
        CANVAS_HEIGHT = self.CANVAS_HEIGHT;

        # UPDATE Y VELOCITY - 
        if (((yCenter + radius) >= CANVAS_HEIGHT) and (yVelocity > 0)):
            self.reset();
        elif (((yCenter - radius) <= 0) and (yVelocity < 0)):
            self.reset();
        else: 
            self.yCenter += yVelocity

        # UPDATE X VELOCITY -
        if (((xCenter - radius) <= 0) and (xVelocity < 0)):
            self.reset();
        elif(((xCenter + radius) >= CANVAS_WIDTH) and (xVelocity > 0)):
            self.reset();
        else: 
            self.xCenter += xVelocity; 

    def deflectOffPaddle(self, paddleCenter, paddleWidth, paddleOrientation):
        xVelocity = self.xVelocity;
        yVelocity = self.yVelocity;

        speed = self.CANVAS_WIDTH // 100;

        offsetFactor = random.uniform(1, 1.1);
        offset = random.uniform(-0.1, 0.1);

        if(paddleOrientation == Orientation.DIR_NORTH):
            speedFactor = (self.xCenter - paddleCenter) / paddleWidth;
            self.xVelocity = speed * speedFactor * offsetFactor + offset;
            self.yVelocity = speed;   
            self.randomColor();         
        
        elif(paddleOrientation == Orientation.DIR_SOUTH):
            speedFactor = (self.xCenter - paddleCenter) / paddleWidth;
            self.xVelocity = speed * speedFactor * offsetFactor + offset;
            self.yVelocity = (-speed);
            self.randomColor();         
        
        elif(paddleOrientation == Orientation.DIR_EAST):
            speedFactor = (self.yCenter - paddleCenter) / paddleWidth;
            self.xVelocity = (-speed);
            self.yVelocity = speed * speedFactor * offsetFactor + offset;
            self.randomColor();         
        
        elif(paddleOrientation == Orientation.DIR_WEST):
            speedFactor = (self.yCenter - paddleCenter) / paddleWidth;
            self.xVelocity = speed;
            self.yVelocity = speed * speedFactor * offsetFactor + offset;
            self.randomColor();         

    def getVelocity(self):
        return  (self.xVelocity, self.yVelocity);

    # draw the ball
    def draw(self, canvas):
        BORDER_WIDTH = self.BORDER_WIDTH;
        color   = self.color;
        xCenter = self.xCenter;
        yCenter = self.yCenter;
        radius  = self.radius;

        canvas.create_oval(xCenter - radius,
                            yCenter - radius,
                            xCenter + radius,
                            yCenter + radius,
                            fill = color, width = BORDER_WIDTH)

    def updateSplash(self, canvas): 
        self.moveSplash(); 
        self.draw(canvas);

    def updateGame(self, canvas):
        self.moveGame();
        self.draw(canvas);

    def getInfo(self): 
        return(self.xCenter, self.yCenter, self.radius);


