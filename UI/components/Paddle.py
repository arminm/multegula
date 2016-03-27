
import random
from enum import Enum
from components.ComponentDefs import *

class Paddle:
    def __init__(self, canvas_width, canvas_height, orientation, state):
        self.CANVAS_WIDTH = canvas_width;
        self.CANVAS_HEIGHT = canvas_height;
        self.MARGIN = canvas_width // 30;
        self.PADDLE_MARGIN = canvas_height // 20;
        self.PADDLE_HEIGHT = canvas_height // 50;   
        self.MIN = self.PADDLE_MARGIN + (2*self.PADDLE_HEIGHT);
        self.MAX = canvas_width - self.PADDLE_MARGIN - (2*self.PADDLE_HEIGHT);   
        self.BORDER_WIDTH = canvas_width // 350;
        self.ORIENTATION = orientation;
        self.width = canvas_width // 6;
        self.center = canvas_width // 2;
        self.speed = canvas_width // 70; 
        self.direction = Direction.DIR_STOP;
        self.state = state;

        self.COLORS = ["red", "green", "blue", "purple", "orange", "yellow", "black", "white"];
        self.color = "black";
        self.randomColor();

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

    def setDirection(self, direction):
        self.direction = direction;

    def move(self):
        MIN = self.MIN;
        MAX = self.MAX;

        if(self.direction == Direction.DIR_LEFT):
            if((self.center - self.width) > self.MIN):
                self.center = self.center - self.speed;
        elif(self.direction == Direction.DIR_RIGHT):
            if((self.center + self.width) < self.MAX):
                self.center = self.center + self.speed;

    def draw(self, canvas): 
        BORDER_WIDTH = self.BORDER_WIDTH; 
        color = self.color;

        (leftEdge, rightEdge, topEdge, bottomEdge) = self.getEdges();

        canvas.create_rectangle(leftEdge, topEdge, rightEdge, bottomEdge,
                                fill = color, width = BORDER_WIDTH);

    def update(self, canvas):
        state = self.state;

        if((state == PlayerState.USER) or (state == PlayerState.AI)):
            self.move();
            self.draw(canvas);
        elif(state == PlayerState.COMP):
            self.draw(canvas);

    def getInfo(self):
        return (self.center, self.width, self.direction, self.ORIENTATION);

    def getEdges(self):
        CANVAS_HEIGHT = self.CANVAS_HEIGHT;
        CANVAS_WIDTH = self.CANVAS_WIDTH;
        PADDLE_MARGIN = self.PADDLE_MARGIN;
        PADDLE_HEIGHT = self.PADDLE_HEIGHT;
        BORDER_WIDTH = self.BORDER_WIDTH; 

        center = self.center;
        width = self.width;
        
        if(self.ORIENTATION == Orientation.DIR_NORTH):

            leftEdge    = center - width;
            rightEdge   = center + width;
            topEdge     = PADDLE_MARGIN;
            bottomEdge  = PADDLE_MARGIN + PADDLE_HEIGHT;     

        elif(self.ORIENTATION == Orientation.DIR_SOUTH):

            leftEdge    = center - width;
            rightEdge   = center + width;
            topEdge     = CANVAS_HEIGHT - PADDLE_HEIGHT - PADDLE_MARGIN;
            bottomEdge  = CANVAS_HEIGHT - PADDLE_MARGIN;

        elif(self.ORIENTATION == Orientation.DIR_EAST):
            leftEdge    = CANVAS_WIDTH - PADDLE_MARGIN - PADDLE_HEIGHT;
            rightEdge   = CANVAS_WIDTH - PADDLE_MARGIN;
            topEdge     = center - width;
            bottomEdge  = center + width; 

        elif(self.ORIENTATION == Orientation.DIR_WEST):
            leftEdge    = PADDLE_MARGIN;
            rightEdge   = PADDLE_MARGIN + PADDLE_HEIGHT;
            topEdge     = center - width;
            bottomEdge  = center + width;

        return (leftEdge, rightEdge, topEdge, bottomEdge);




