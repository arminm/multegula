from enum import Enum
from components.Paddle import *
from components.ComponentDefs import *
from screens.ScreenEnum import *

class Player:
    def __init__(self, canvas_width, canvas_height, orientation, state):
        self.CANVAS_HEIGHT = canvas_height;
        self.CANVAS_WIDTH = canvas_width;
        self.ORIENTATION = orientation;
        self.state = state;
        self.score = 0;
        self.lives = 5;
        self.power = PowerUps.PWR_NONE;
        self.paddle = Paddle(canvas_width, canvas_height, orientation, state);


    def setDirection(self, direction):
        self.paddle.setDirection(direction);

    def AI(self, canvas):
        (ballCenterX, ballCenterY, ballRadius) = canvas.data["ball"].getInfo();
        (paddleCenter, paddleWidth, paddleDir, paddleOrientation) = self.paddle.getInfo();

        offset = paddleWidth // 5;

        if(paddleOrientation == Orientation.DIR_NORTH):
            direction = paddleCenter - ballCenterX;
        elif(paddleOrientation == Orientation.DIR_WEST):
            direction = paddleCenter - ballCenterY;
        elif(paddleOrientation == Orientation.DIR_EAST):
            direction = paddleCenter - ballCenterY;

        chance = random.randint(0, 4);

        if((abs(direction) > offset) and (paddleDir == Direction.DIR_STOP) and (chance == 1)): 
            if(direction < offset):
                self.paddle.setDirection(Direction.DIR_RIGHT);
            elif(direction > offset):
                self.paddle.setDirection(Direction.DIR_LEFT);
        elif(chance == 0):
            self.paddle.setDirection(Direction.DIR_STOP);

    def updateBall(self, canvas):
        CANVAS_HEIGHT = self.CANVAS_HEIGHT;
        CANVAS_WIDTH = self.CANVAS_WIDTH;
        ORIENTATION = self.ORIENTATION;
        ballReset = False;
        ballBounce = False;


        (ballCenterX, ballCenterY, ballRadius) = canvas.data["ball"].getInfo();
        (leftEdge, rightEdge, topEdge, bottomEdge) = self.paddle.getEdges();
        (paddleCenter, paddleWidth, paddleDir, paddleOrientation) = self.paddle.getInfo();

        if(ORIENTATION == Orientation.DIR_NORTH):
            # ball out of bounts on NORTH edge
            if((ballCenterY - ballRadius) <= 0):
                ballReset = True;
            # ball deflected by 
            elif((leftEdge <= ballCenterX <= rightEdge) and (topEdge <= (ballCenterY - ballRadius) < bottomEdge)): 
                ballBounce = True;
        elif(ORIENTATION == Orientation.DIR_SOUTH):
            if((ballCenterY + ballRadius) >= CANVAS_HEIGHT): 
                ballReset = True;
            elif((leftEdge <= ballCenterX <= rightEdge) and (topEdge <= (ballCenterY + ballRadius) < bottomEdge)): 
                ballBounce = True;
        elif(ORIENTATION == Orientation.DIR_EAST):
            if((ballCenterX + ballRadius) >= CANVAS_WIDTH):
                ballReset = True;
            elif((topEdge <= ballCenterY <= bottomEdge) and (leftEdge <= (ballCenterX + ballRadius) < rightEdge)):
                ballBounce = True;
        elif(ORIENTATION == Orientation.DIR_WEST):
            if((ballCenterX - ballRadius) <= 0):
                ballReset = True;
            elif((topEdge <= ballCenterY <= bottomEdge) and (leftEdge <= (ballCenterX - ballRadius) < rightEdge)):
                ballBounce = True;

        if(ballReset):
            canvas.data["ball"].reset();
            canvas.data["currentScreen"] = Screens.SCRN_PAUSE;
            canvas.data["nextScreen"] = Screens.SCRN_GAME;
            self.lives -= 1;
            self.score -= 20;
        elif(ballBounce):
            canvas.data["ball"].deflectOffPaddle(paddleCenter, paddleWidth, paddleOrientation);    
            self.score += 3; 

    def displayStatus(self, canvas):
        ORIENTATION = self.ORIENTATION;
        CANVAS_HEIGHT = self.CANVAS_HEIGHT;
        CANVAS_WIDTH = self.CANVAS_WIDTH;
        X_MARGIN = CANVAS_WIDTH // 60;
        Y_MARGIN = CANVAS_HEIGHT // 60;

        statusMsg = "";

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

        
        statusMsg += "P/" + str(self.score) + ".  L/" + str(self.lives) + ".";

        canvas.create_text(X_LOC, Y_LOC, text = statusMsg,
                font = ("Courier", canvas.data["S_TEXT_SIZE"]), fill = "white");


    def update(self, canvas):
        if(self.state == PlayerState.AI):
            self.AI(canvas);
        self.paddle.update(canvas);
        self.updateBall(canvas);
        self.displayStatus(canvas);



