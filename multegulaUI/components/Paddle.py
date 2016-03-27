# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# Paddle.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
import random
from enum import Enum
from components.ComponentDefs import *

# PADDLE class
class Paddle:
    ### __init__ - initialize and return a paddle
    ##  @param canvas_width
    ##  @param canvas_height
    ##  @param orientation - location on the screen of this padde (DIR_NORTH/DIR_SOUTH/...)
    ##  @param state - current control state of the player (USER/AI/COMP)
    def __init__(self, canvas_width, canvas_height, orientation, state):
        # CONSTANT fields
        self.CANVAS_WIDTH = canvas_width;
        self.CANVAS_HEIGHT = canvas_height;
        self.MARGIN = canvas_width // 30;
        self.PADDLE_MARGIN = canvas_height // 20;
        self.PADDLE_HEIGHT = canvas_height // 50;   
        self.MIN = self.PADDLE_MARGIN + (2*self.PADDLE_HEIGHT);
        self.MAX = canvas_width - self.PADDLE_MARGIN - (2*self.PADDLE_HEIGHT);   
        self.BORDER_WIDTH = canvas_width // 350;
        self.ORIENTATION = orientation;
        self.COLORS = ["red", "green", "blue", "purple", "orange", "yellow", "black", "white"];

        # dynamic fields
        self.state = state;
        self.speed = canvas_width // 70; 
        self.direction = Direction.DIR_STOP;
        self.center = canvas_width // 2;
        self.width = canvas_width // 6;
        self.color = "black";
        self.randomColor();

    #### get/set STATE methods
    def setState(self, state):
        self.state = state;

    def getState(self):
        return self.state;

    #### get/set SPEED methods
    def setSpeed(self, speed):
        self.speed = speed;

    def increaseSpeed(self):
        self.speed *= 1.1;

    def decreaseSpeed(self):
        self.speed *= 0.9;

    def getSpeed(self):
        return self.speed;

    #### get/set DIRECTION methods
    def setDirection(self, direction):
        self.direction = direction;

    def getDirection(self):
        return self.direction;

    #### get/set CENTER methods
    def setCenter(self, center):
        self.center = center;

    def getCenter(self):
        return self.center;

    ### get/set WIDTH methods
    def setWidth(self, width):
        self.width = width;

    def increaseWidth(self):
        self.width *= 1.1;

    def decreaseWidth(self):
        self.width -= 0.9;

    def getWidth(self):
        return self.width;

    ### get/set COLOR methods
    def randomColor(self):
        currentColor = self.color;
        newColor = currentColor;

        # loop until a new color has been chosen
        while (currentColor == newColor):
            newColor = random.choice(self.COLORS);

        # set new color
        self.color = newColor;

    def setColor(self, color):
        self.color = color;

    def getColor(self):
        return self.color;

    ### move - move the paddle based on the current direction
    def move(self):
        MIN = self.MIN;
        MAX = self.MAX;

        # move paddle left if not already at the MIN possible
        if(self.direction == Direction.DIR_LEFT):
            if((self.center - self.width) > self.MIN):
                self.center = self.center - self.speed;
        # move paddle right if not already at the MAX possible
        elif(self.direction == Direction.DIR_RIGHT):
            if((self.center + self.width) < self.MAX):
                self.center = self.center + self.speed;
        # implicit else - do nothing

    ### draw - draw the paddle
    def draw(self, canvas): 
        (leftEdge, rightEdge, topEdge, bottomEdge) = self.getEdges();

        canvas.create_rectangle(leftEdge, topEdge, rightEdge, bottomEdge,
                                fill = self.color, width = self.BORDER_WIDTH);

    ### update - update the paddle location (that is, 'move' if applicable) and draw
    def update(self, canvas):
        state = self.state;

        if((state == PlayerState.USER) or (state == PlayerState.AI)):
            self.move();
            self.draw(canvas);
        elif(state == PlayerState.COMP):
            self.draw(canvas);

    ### getInfo - get pertinent information about the paddle
    def getInfo(self):
        return (self.center, self.width, self.direction, self.ORIENTATION);

    ### getEdges - get the edges of the paddle based on the orientation
    def getEdges(self):
        CANVAS_HEIGHT = self.CANVAS_HEIGHT;
        CANVAS_WIDTH = self.CANVAS_WIDTH;
        PADDLE_MARGIN = self.PADDLE_MARGIN;
        PADDLE_HEIGHT = self.PADDLE_HEIGHT;
        BORDER_WIDTH = self.BORDER_WIDTH; 

        center = self.center;
        width = self.width;
        
        # edges of the NORTH paddle
        if(self.ORIENTATION == Orientation.DIR_NORTH):
            leftEdge    = center - width;
            rightEdge   = center + width;
            topEdge     = PADDLE_MARGIN;
            bottomEdge  = PADDLE_MARGIN + PADDLE_HEIGHT;     

        # edges of the SOUTH paddle
        elif(self.ORIENTATION == Orientation.DIR_SOUTH):
            leftEdge    = center - width;
            rightEdge   = center + width;
            topEdge     = CANVAS_HEIGHT - PADDLE_HEIGHT - PADDLE_MARGIN;
            bottomEdge  = CANVAS_HEIGHT - PADDLE_MARGIN;

        # edges of the EAST paddle
        elif(self.ORIENTATION == Orientation.DIR_EAST):
            leftEdge    = CANVAS_WIDTH - PADDLE_MARGIN - PADDLE_HEIGHT;
            rightEdge   = CANVAS_WIDTH - PADDLE_MARGIN;
            topEdge     = center - width;
            bottomEdge  = center + width; 

        # edges of the WEST paddle
        elif(self.ORIENTATION == Orientation.DIR_WEST):
            leftEdge    = PADDLE_MARGIN;
            rightEdge   = PADDLE_MARGIN + PADDLE_HEIGHT;
            topEdge     = center - width;
            bottomEdge  = center + width;

        return (leftEdge, rightEdge, topEdge, bottomEdge);




