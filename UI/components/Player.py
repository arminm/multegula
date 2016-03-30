# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# Player.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
import random
from enum import Enum
from components.Paddle import *
from components.ComponentDefs import *
from screens.ScreenEnum import *

# PLAYER class
class Player:
    ### __init__  - initialize and return Player
    ##  @param canvas_width
    ##  @param canvas_height
    ##  @param orientation - location on the screen of this padde (DIR_NORTH/DIR_SOUTH/...)
    ##  @param state - current control state of the player (USER/AI/COMP)
    def __init__(self, canvas_width, canvas_height, orientation, state):
        self.CANVAS_HEIGHT = canvas_height;
        self.CANVAS_WIDTH = canvas_width;
        self.ORIENTATION = orientation;
        self.state = state;
        self.score = 0;
        self.lives = 5;
        self.power = PowerUps.PWR_NONE;
        self.paddle = Paddle(canvas_width, canvas_height, orientation, state);
        self.first = True;
        self.statusUpdate = False;

    ### get/set direction methods
    def setDirection(self, direction):
        self.paddle.setDirection(direction);

    def getDirection(self):
        return self.paddle.getDirection();

    ### AI method -
    ##  This method moves the paddles automatically to contact the ball. There are some
    ##  non-idealities built in so the computer is not perfect
    def AI(self, canvas):
        # get ball/paddle information
        (ballCenterX, ballCenterY, ballRadius) = canvas.data["ball"].getInfo();
        (paddleCenter, paddleWidth, paddleDir, paddleOrientation) = self.paddle.getInfo();

        # calcualte an offset and a random number - used to create a delay in the paddle response
        offset = paddleWidth // 5;
        chance = random.randint(0, 4);

        # determine which direction the ball in from the center of the paddle based on the
        #   current orientation.
        if((paddleOrientation == Orientation.DIR_NORTH) or (paddleOrientation == Orientation.DIR_SOUTH)):
            direction = paddleCenter - ballCenterX;
        elif((paddleOrientation == Orientation.DIR_WEST) or (paddleOrientation == Orientation.DIR_EAST)):
            direction = paddleCenter - ballCenterY;

        # MOVE the paddle -
        ## if the ball has moved at least 'offset' distance from the center of the paddle, 
        ##  the paddle is currently stopped, and it's your lucky day -> move the paddle
        if((abs(direction) > offset) and (paddleDir == Direction.DIR_STOP) and (chance == 1)): 
            if(direction < offset):
                self.paddle.setDirection(Direction.DIR_RIGHT);
            elif(direction > offset):
                self.paddle.setDirection(Direction.DIR_LEFT);
        ## otherwise, if it's your lucky day -> stop the paddle
        elif(chance == 0):
            self.paddle.setDirection(Direction.DIR_STOP);

    ### updateBall method - 
    ##  Check to see if the ball is off the playing field or is being deflected by the player's paddle.
    def updateBall(self, canvas):
        # get canvas/paddle/ball info
        CANVAS_HEIGHT = self.CANVAS_HEIGHT;
        CANVAS_WIDTH = self.CANVAS_WIDTH;
        ORIENTATION = self.ORIENTATION;
        (ballCenterX, ballCenterY, ballRadius) = canvas.data["ball"].getInfo();
        (leftEdge, rightEdge, topEdge, bottomEdge) = self.paddle.getEdges();
        (paddleCenter, paddleWidth, paddleDir, paddleOrientation) = self.paddle.getInfo();

        # initialize flags
        ballReset = False;
        ballBounce = False;

        # ball out of bounds/deflected on NORTH edge/paddle
        if(ORIENTATION == Orientation.DIR_NORTH):
            if((ballCenterY - ballRadius) <= 0):
                ballReset = True;
            elif(((leftEdge <= (ballCenterX + ballRadius) < rightEdge) and (topEdge <= (ballCenterY - ballRadius) < bottomEdge)) or 
                    (leftEdge < ((ballCenterX - ballRadius) <= rightEdge) and (topEdge <= (ballCenterY - ballRadius) < bottomEdge))):
                ballBounce = True;

        # ball out of bounds/deflected on the SOUTH edge/paddle
        elif(ORIENTATION == Orientation.DIR_SOUTH):
            if((ballCenterY + ballRadius) >= CANVAS_HEIGHT): 
                ballReset = True;
            elif(((leftEdge <= (ballCenterX + ballRadius) < rightEdge) and (topEdge <= (ballCenterY + ballRadius) < bottomEdge)) or 
                    (leftEdge < ((ballCenterX - ballRadius) <= rightEdge) and (topEdge <= (ballCenterY + ballRadius) < bottomEdge))):
                ballBounce = True;

        # ball out of bounds/deflected on the EAST edge/paddle
        elif(ORIENTATION == Orientation.DIR_EAST):
            if((ballCenterX + ballRadius) >= CANVAS_WIDTH):
                ballReset = True;
            elif(((topEdge <= (ballCenterY + ballRadius) < bottomEdge) and (leftEdge <= (ballCenterX + ballRadius) < rightEdge)) or
                    (topEdge < ((ballCenterX - ballRadius) <= bottomEdge) and (leftEdge <= (ballCenterX + ballRadius) < rightEdge))):
                ballBounce = True;

        # ball out of bounds/deflected on the WEST edge/paddle
        elif(ORIENTATION == Orientation.DIR_WEST):
            # out of play
            if((ballCenterX - ballRadius) <= 0):
                ballReset = True;
            elif(((topEdge <= (ballCenterY + ballRadius) < bottomEdge) and (leftEdge <= (ballCenterX - ballRadius) < rightEdge)) or
                    (topEdge < ((ballCenterX - ballRadius) <= bottomEdge) and (leftEdge <= (ballCenterX - ballRadius) < rightEdge))):
                ballBounce = True;


        # reset ball, apply appropriate scoring
        if(ballReset):
            canvas.data["ball"].reset();
            canvas.data["currentScreen"] = Screens.SCRN_PAUSE;
            canvas.data["nextScreen"] = Screens.SCRN_GAME;
            self.lives -= 1;
            self.score -= 20;
            self.statusUpdate = True;
        # bounce ball, apply appropriate scoring
        elif(ballBounce):
            self.deflectOffPaddle(canvas);    
            self.score += 3; 
            self.statusUpdate = True;
        # implicit else - do nothing

    ### deflectOffPaddle - 
    ##  Deflect ball off of a paddle and determine the new direction off the ball
    def deflectOffPaddle(self, canvas):
        # initialize speed and random offset variables
        speed = self.CANVAS_WIDTH // 110;
        offsetFactor = random.uniform(1, 1.1);
        offset = random.uniform(-0.1, 0.1);

        # get ball/paddle info
        (paddleCenter, paddleWidth, paddleDir, paddleOrientation) = self.paddle.getInfo();
        (ballCenterX, ballCenterY, ballRadius) = canvas.data["ball"].getInfo();

        # deflect off NORTH paddle
        if(paddleOrientation == Orientation.DIR_NORTH):
            speedFactor = (ballCenterX - paddleCenter) / paddleWidth;
            xVelocity = speed * speedFactor * offsetFactor + offset;
            yVelocity = speed;        

        
        # deflect off SOUTH paddle
        elif(paddleOrientation == Orientation.DIR_SOUTH):
            speedFactor = (ballCenterX - paddleCenter) / paddleWidth;
            xVelocity = speed * speedFactor * offsetFactor + offset;
            yVelocity = (-speed);

        # deflect off EAST paddle
        elif(paddleOrientation == Orientation.DIR_EAST):
            speedFactor = (ballCenterY - paddleCenter) / paddleWidth;
            xVelocity = (-speed);
            yVelocity = speed * speedFactor * offsetFactor + offset;
        
        # deflect off WEST paddle
        elif(paddleOrientation == Orientation.DIR_WEST):
            speedFactor = (ballCenterY - paddleCenter) / paddleWidth;
            xVelocity = speed;
            yVelocity = speed * speedFactor * offsetFactor + offset;
            
        canvas.data["ball"].setVelocity(xVelocity, yVelocity);  
        canvas.data["ball"].randomColor();
 

    def setStatus(self, canvas):
        # get canvas info
        ORIENTATION = self.ORIENTATION;
        CANVAS_HEIGHT = self.CANVAS_HEIGHT;
        CANVAS_WIDTH = self.CANVAS_WIDTH;
        X_MARGIN = CANVAS_WIDTH // 60;
        Y_MARGIN = CANVAS_HEIGHT // 60;

        # initilize status message
        statusMsg = "";

        # determin X_LOC, Y_LOC, and NAME based on orientation
        if(ORIENTATION == Orientation.DIR_NORTH):
            X_LOC = CANVAS_WIDTH*0.25;
            Y_LOC = Y_MARGIN;
            statusMsg += "NoRTH: "
        elif(ORIENTATION == Orientation.DIR_SOUTH):
            X_LOC = CANVAS_WIDTH*0.75;
            Y_LOC = CANVAS_HEIGHT - Y_MARGIN;
            statusMsg += (canvas.data["playerName"] + " ");

        elif(ORIENTATION == Orientation.DIR_EAST):
            X_LOC = CANVAS_WIDTH*0.75;
            Y_LOC = Y_MARGIN;    
            statusMsg += "eaST: "

        elif(ORIENTATION == Orientation.DIR_WEST):
            X_LOC = CANVAS_WIDTH*0.25;
            Y_LOC = CANVAS_HEIGHT - Y_MARGIN;
            statusMsg += "WeST: "

        # finish status message and display
        statusMsg += "P/" + str(self.score) + ".  L/" + str(self.lives) + ".";
        self.t = canvas.create_text(X_LOC, Y_LOC, text = statusMsg,
                                    font = ("Courier", canvas.data["S_TEXT_SIZE"]), fill = "white");
    ### displayStatus method -
    ##  Display the text for the player indicating the current score and number of lives remaining
    def displayStatus(self, canvas):
        if(not(self.first) and self.statusUpdate):
            canvas.delete(self.t);
            self.setStatus(canvas);
            self.statusUpdate = False;
        elif(self.first):
            self.setStatus(canvas);
            self.first = False;

    ### general purpose update
    def update(self, canvas):
        # Human player update
        if(self.state == PlayerState.USER):
            self.paddle.update(canvas);
            self.updateBall(canvas);
            self.displayStatus(canvas);
        # Artificial player update
        elif(self.state == PlayerState.AI):
            self.AI(canvas);
            self.paddle.update(canvas);
            self.updateBall(canvas);
            self.displayStatus(canvas);
        # Only competitor update
        elif(self.state == PlayerState.COMP):
            self.paddle.draw(canvas);
            self.displayStatus(canvas);
