
import random
from enum import Enum
from components.ComponentDefs import *


class PaddleState(Enum):
    USER = 0;   # controlled by this player
    AI = 1;     # controlling it self
    COMP = 2;   # controlled by a COMPetitor

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
        CANVAS_HEIGHT = self.CANVAS_HEIGHT;
        CANVAS_WIDTH = self.CANVAS_WIDTH;
        PADDLE_MARGIN = self.PADDLE_MARGIN;
        PADDLE_HEIGHT = self.PADDLE_HEIGHT;
        BORDER_WIDTH = self.BORDER_WIDTH; 

        center = self.center;
        width = self.width;
        color = self.color;

        if(self.ORIENTATION == Orientation.DIR_NORTH):
            leftEdge    = center - width;
            rightEdge   = center + width;
            topEdge     = PADDLE_MARGIN;
            bottomEdge  = PADDLE_MARGIN + PADDLE_HEIGHT;

        # draw paddle at the bottom of the screen
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

        # draw paddle on the left
        elif(self.ORIENTATION == Orientation.DIR_WEST):
            leftEdge    = PADDLE_MARGIN;
            rightEdge   = PADDLE_MARGIN + PADDLE_HEIGHT;
            topEdge     = center - width;
            bottomEdge  = center + width;

        canvas.create_rectangle(leftEdge, topEdge, rightEdge, bottomEdge,
                                fill = color, width = BORDER_WIDTH);

    def deflectBall(self, canvas):
        CANVAS_HEIGHT = self.CANVAS_HEIGHT;
        CANVAS_WIDTH = self.CANVAS_WIDTH;
        PADDLE_MARGIN = self.PADDLE_MARGIN;
        PADDLE_HEIGHT = self.PADDLE_HEIGHT;
        BORDER_WIDTH = self.BORDER_WIDTH; 

        center = self.center;
        width = self.width;
        
        (ballCenterX, ballCenterY, ballRadius) = canvas.data["ball"].getInfo();

        if(self.ORIENTATION == Orientation.DIR_NORTH):

            leftEdge    = center - width;
            rightEdge   = center + width;
            topEdge     = PADDLE_MARGIN;
            bottomEdge  = PADDLE_MARGIN + PADDLE_HEIGHT;  

            if((leftEdge <= ballCenterX <= rightEdge) and (topEdge <= (ballCenterY - ballRadius) < bottomEdge)): 
                canvas.data["ball"].deflectOffPaddle(center, width, self.ORIENTATION);     

        elif(self.ORIENTATION == Orientation.DIR_SOUTH):

            leftEdge    = center - width;
            rightEdge   = center + width;
            topEdge     = CANVAS_HEIGHT - PADDLE_HEIGHT - PADDLE_MARGIN;
            bottomEdge  = CANVAS_HEIGHT - PADDLE_MARGIN;

            if((leftEdge <= ballCenterX <= rightEdge) and (topEdge <= (ballCenterY + ballRadius) < bottomEdge)): 
                canvas.data["ball"].deflectOffPaddle(center, width, self.ORIENTATION);  

        elif(self.ORIENTATION == Orientation.DIR_EAST):
            leftEdge    = CANVAS_WIDTH - PADDLE_MARGIN - PADDLE_HEIGHT;
            rightEdge   = CANVAS_WIDTH - PADDLE_MARGIN;
            topEdge     = center - width;
            bottomEdge  = center + width;

            if((topEdge <= ballCenterY <= bottomEdge) and (leftEdge <= (ballCenterX + ballRadius) < rightEdge)):
                canvas.data["ball"].deflectOffPaddle(center, width, self.ORIENTATION);  

        elif(self.ORIENTATION == Orientation.DIR_WEST):
            leftEdge    = PADDLE_MARGIN;
            rightEdge   = PADDLE_MARGIN + PADDLE_HEIGHT;
            topEdge     = center - width;
            bottomEdge  = center + width;

            if((topEdge <= ballCenterY <= bottomEdge) and (leftEdge <= (ballCenterX - ballRadius) < rightEdge)):
                canvas.data["ball"].deflectOffPaddle(center, width, self.ORIENTATION);  

    def AI(self, canvas):
        (ballCenterX, ballCenterY, ballRadius) = canvas.data["ball"].getInfo();
        center = self.center;
        offset = self.width // 4;
        currentDir = self.direction;
        orientation = self.ORIENTATION;

        if(orientation == Orientation.DIR_NORTH):
            direction = center - ballCenterX;
        elif(orientation == Orientation.DIR_WEST):
            direction = center - ballCenterY;
        elif(orientation == Orientation.DIR_EAST):
            direction = center - ballCenterY;

        chance = random.randint(0, 5);

        if((abs(direction) > offset) and (currentDir == Direction.DIR_STOP) and (chance == 1)): 
            if(direction < offset):
                self.setDirection(Direction.DIR_RIGHT);
            elif(direction > offset):
                self.setDirection(Direction.DIR_LEFT);
        elif(chance == 0):
            self.setDirection(Direction.DIR_STOP);

    def update(self, canvas):
        state = self.state;

        if(state == PaddleState.USER):
            self.move();
            self.deflectBall(canvas);
        elif(state == PaddleState.AI):
            self.AI(canvas);
            self.move();
            self.deflectBall(canvas);

        self.draw(canvas);





