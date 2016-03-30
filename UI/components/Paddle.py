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
        self.MARGIN = canvas_height // 20;
        self.HEIGHT = canvas_height // 50;   
        self.MIN = self.MARGIN + (2*self.HEIGHT);
        self.MAX = canvas_width - self.MARGIN - (2*self.HEIGHT);   
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
        self.redraw = False;
        self.first = True;

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
        self.redraw = True;

    def decreaseWidth(self):
        self.width -= 0.9;
        self.redraw = True;

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
        self.redraw = True;

    def setColor(self, color):
        self.color = color;
        self.redraw = True;

    def getColor(self):
        return self.color;

    ### move - move the paddle based on the current direction
    def move(self):
        MIN = self.MIN;
        MAX = self.MAX;

        # move paddle left if not already at the MIN possible
        if((self.direction == Direction.DIR_LEFT) and ((self.center - self.width) > self.MIN)):
            self.center = self.center - self.speed;
            self.redraw = True;
        # move paddle right if not already at the MAX possible
        elif((self.direction == Direction.DIR_RIGHT) and ((self.center + self.width) < self.MAX)):
            self.center = self.center + self.speed;
            self.redraw = True;
        else:
            self.redraw = False;

    def setPaddle(self, canvas):
        (leftEdge, rightEdge, topEdge, bottomEdge) = self.getEdges();
        self.p = canvas.create_rectangle(leftEdge, topEdge, rightEdge, bottomEdge,
                                            fill = self.color, width = self.BORDER_WIDTH);
    ### draw - draw the paddle
    def draw(self, canvas): 
        if(not(self.first) and self.redraw):
            canvas.delete(self.p);
            self.setPaddle(canvas);
            self.redraw = False;
        elif(self.first):
            self.setPaddle(canvas);
            self.first = False;

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
        MARGIN = self.MARGIN;
        HEIGHT = self.HEIGHT;
        BORDER_WIDTH = self.BORDER_WIDTH; 

        center = self.center;
        width = self.width;
        
        # edges of the NORTH paddle
        if(self.ORIENTATION == Orientation.DIR_NORTH):
            leftEdge    = center - width;
            rightEdge   = center + width;
            topEdge     = MARGIN;
            bottomEdge  = MARGIN + HEIGHT;     

        # edges of the SOUTH paddle
        elif(self.ORIENTATION == Orientation.DIR_SOUTH):
            leftEdge    = center - width;
            rightEdge   = center + width;
            topEdge     = CANVAS_HEIGHT - HEIGHT - MARGIN;
            bottomEdge  = CANVAS_HEIGHT - MARGIN;

        # edges of the EAST paddle
        elif(self.ORIENTATION == Orientation.DIR_EAST):
            leftEdge    = CANVAS_WIDTH - MARGIN - HEIGHT;
            rightEdge   = CANVAS_WIDTH - MARGIN;
            topEdge     = center - width;
            bottomEdge  = center + width; 

        # edges of the WEST paddle
        elif(self.ORIENTATION == Orientation.DIR_WEST):
            leftEdge    = MARGIN;
            rightEdge   = MARGIN + HEIGHT;
            topEdge     = center - width;
            bottomEdge  = center + width;

        # left right top 
        return (leftEdge, rightEdge, topEdge, bottomEdge);




