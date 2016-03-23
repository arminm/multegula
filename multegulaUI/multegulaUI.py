# EXAMPLE UI CODE FROM BLOCKBUSTER
# For porting to Multegula
# Adapted for Python 3 by Garrett Miller and 2to3 utility
# 
# Originally by daniel santoro. ddsantor.

##### IMPORT MODULES #####
from tkinter import *
import random
##### END IMPORT MODULES ######

"""
This next large section of code is responsible for everything that has to
deal with the splash screen.  In the case of this program, this, more
specifically, deals with anything that isn't playing the game.  I found that
using one giant function with it's own timer made it easy to separate what was
the game and what wasn't the game, as well as turn the splash screen on and
off fairly simply.  Also, this format allows me to only pass the canvas to
the splash screen function and none of it's many helper functions because of
the way that local functions work.  This was a very nice convenience.
"""

##########################
##### SPLASH SCREEN ######

## SPLASH SCREEN: takes "canvas", returns None
## # this does everything with regards to the splash screen
def splashScreen(canvas):
  # EXTRACT information from the canvas
  # # canvas variables
  CANVAS_HEIGHT = canvas.data["CANVAS_HEIGHT"]
  CANVAS_WIDTH = canvas.data["CANVAS_WIDTH"]
  
  # # button variables
  BUTTON_COLOR_ACTIVE   = canvas.data["BUTTON_COLOR_ACTIVE"]
  BUTTON_COLOR_INACTIVE = canvas.data["BUTTON_COLOR_INACTIVE"]
  BUTTON_X_SIZE = canvas.data["BUTTON_X_SIZE"];
  BUTTON_Y_SIZE = canvas.data["BUTTON_Y_SIZE"];
  BUTTON_MARGIN = canvas.data["BUTTON_MARGIN"];

  # # text locations 
  Y_LOC_TITLE         = canvas.data["Y_LOC_TITLE"];
  Y_LOC_AUTHOR1       = canvas.data["Y_LOC_AUTHOR1"];
  Y_LOC_AUTHOR2       = canvas.data["Y_LOC_AUTHOR2"];
  Y_LOC_TOP_BUTTON    = canvas.data["Y_LOC_TOP_BUTTON"];
  Y_LOC_BOTTOM_BUTTON = canvas.data["Y_LOC_BOTTOM_BUTTON"];
  
  # # text sizes
  S_TEXT_SIZE   = canvas.data["S_TEXT_SIZE"];
  M_TEXT_SIZE   = canvas.data["M_TEXT_SIZE"];
  L_TEXT_SIZE   = canvas.data["L_TEXT_SIZE"];
  XL_TEXT_SIZE  = canvas.data["XL_TEXT_SIZE"];
  
  # # ball variables  
  SPLASH_RADIUS = canvas.data["SPLASH_RADIUS"];
  ballCenterY   = canvas.data["ballCenterY"];

  # general location variables
  X_CENTER  = CANVAS_WIDTH // 2;
  Y_CENTER  = CANVAS_HEIGHT // 2;
  X_MARGIN  = CANVAS_WIDTH // 30;
  Y_MARGIN  = CANVAS_HEIGHT // 30;
  
  ## DRAW button: takes the vertical placement of the button, and the lines
  ##              to be written, returns None
  ## # this function draws a button on the canvas. It is called many times
  ## # # by the various 
  def drawButton(xCenter, yCenter, label, color):
    # button border
    canvas.create_rectangle(xCenter - BUTTON_X_SIZE, 
                            yCenter - BUTTON_Y_SIZE,
                            xCenter + BUTTON_X_SIZE,
                            yCenter + BUTTON_Y_SIZE, 
                            fill = "black");

    # button's clickable region
    canvas.create_rectangle(xCenter - BUTTON_X_SIZE + BUTTON_MARGIN,
                            yCenter - BUTTON_Y_SIZE + BUTTON_MARGIN,
                            xCenter + BUTTON_X_SIZE - BUTTON_MARGIN,
                            yCenter + BUTTON_Y_SIZE - BUTTON_MARGIN,
                            fill = color);
    # button text
    canvas.create_text(xCenter, yCenter, text = label,
                        font = ("Courier", S_TEXT_SIZE)); 
      
  ## DRAW the splash screen background: takes nothing, returns None
  ## # this draws the color part of the background over top of the
  ## # # the black background
  def splashScreenBackGround():
    # This variables are called within the function because they changes as the
    # # user clicks certain places.       
    color = canvas.data["SPLASH_SCREEN_COLOR"]

    # black background
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill = "black", width = 0);

    # color foreground
    canvas.create_rectangle(X_MARGIN, Y_MARGIN, CANVAS_WIDTH - X_MARGIN,
                            CANVAS_HEIGHT - Y_MARGIN, fill = color,
                            width = 0);
      
  ## DRAW splash screen text: takes nothing, returns None
  ## # this draws the title and the author over the colored portion of the
  ## # # background.
  def splashScreenText():
    # title
    canvas.create_text(X_CENTER, Y_LOC_TITLE, text = "MULTEGULA",
                        font = ("Courier", XL_TEXT_SIZE));
    # authors
    canvas.create_text(X_CENTER, Y_LOC_AUTHOR1, text = "created by",
                        font = ("Courier", M_TEXT_SIZE));
    canvas.create_text(X_CENTER, Y_LOC_AUTHOR2, text = "DS Team Misfits",
                        font = ("Courier", M_TEXT_SIZE));

  ## DRAW splash screen buttons: takes nothing, returns None
  ## # this uses local functions to draw each button overtop of the colored
  ## # # part of the background
  def splashScreenButtons():
    drawButton(X_CENTER, Y_LOC_TOP_BUTTON, "Solo Game", BUTTON_COLOR_ACTIVE);
    drawButton(X_CENTER, Y_LOC_BOTTOM_BUTTON, "Join Game", BUTTON_COLOR_INACTIVE);

  ## DRAW and MOVE the ball: takes nothing, returns None
  ## # This function does almost everything that pertains to the bouncing
  ## # # ball. From determining it's color, to drawing it, to making it move
  ## # # # this is all accomplished with local functions.
  def ball():
    ## BALL color
    ## # determines the color of the ball, randomly
    def randomizeSplashBallColor():
      # extract information from the dictionary
      currentColor = canvas.data["splashBallColor"];
      
      # BALL color options
      colors = ["red", "white", "green", "blue", "purple", "orange", "yellow"];

      # loop until the conditions are met
      while True:
        color = random.choice(colors);
        if color != canvas.data["SPLASH_SCREEN_COLOR"] and color != currentColor:
          return color;
            
    ## DRAW ball: takes nothing, returns None
    ## # draws the ball...suprise!
    def drawBall():
      # the reason this variables are called here and not with the rest
      # # of the variables at the top of the funtion is because if they
      # # # were called there and not here the ball would not move becuase
      # # # # these variables are constantly changing
      color = canvas.data["splashBallColor"]
      borderWidth = canvas.data["borderWidth"]
      ballCenterX = canvas.data["ballCenterX"]
      ballCenterY = canvas.data["ballCenterY"]

      canvas.create_oval(ballCenterX - SPLASH_RADIUS,
                         ballCenterY - SPLASH_RADIUS,
                         ballCenterX + SPLASH_RADIUS,
                         ballCenterY + SPLASH_RADIUS,
                         fill = color, width = borderWidth)

    ## BALL x velocity determinate: takes nothing, returns None
    ## # determines the x velocity, randomly
    def randomizeXVelocityOfBall():
      velocityFactor = random.random();
      velocityFactor *= random.randint(-2, 2);
      canvas.data["splashBallVX"] = (canvas.data["splashBallVY"] * velocityFactor);

    ## CALL apppropriate velocity function: takes nothing, returns None
    ## # determines with velocity function to call to move the ball in
    ## # # the correct direction
    def updateBallVelocity():
      # these variables need to be called here because they are constantly changing
      ballCenterX = canvas.data["ballCenterX"]
      splashBallVX = canvas.data["splashBallVX"]
      ballCenterY = canvas.data["ballCenterY"]
      splashBallVY = canvas.data["splashBallVY"]

      # UPDATE Y VELOCITY - 
      if (((ballCenterY + SPLASH_RADIUS) >= CANVAS_HEIGHT) and (canvas.data["splashBallVY"] > 0)):
        randomizeXVelocityOfBall()
        canvas.data["splashBallColor"] = randomizeSplashBallColor();
        canvas.data["splashBallVY"] -= (2*splashBallVY);
      elif (((ballCenterY - SPLASH_RADIUS) <= 0) and (canvas.data["splashBallVY"] < 0)):
        canvas.data["splashBallColor"] = randomizeSplashBallColor();
        canvas.data["splashBallVY"] -= (2*splashBallVY);
      else: 
        canvas.data["ballCenterY"] += splashBallVY

      # UPDATE X VELOCITY -
      if (((ballCenterX - SPLASH_RADIUS) <= 0) and (canvas.data["splashBallVX"] < 0)):
        canvas.data["splashBallVX"] -= (splashBallVX*2);
      elif(((ballCenterX + SPLASH_RADIUS) >= CANVAS_WIDTH) and (canvas.data["splashBallVX"] > 0)):
        canvas.data["splashBallVX"] -= (splashBallVX*2);
      else: 
        canvas.data["ballCenterX"] += splashBallVX; 

    # call functions to get the ball moving
    updateBallVelocity()
    drawBall()

  ## TIMER: takes nothing, returns None
  ## # this runs the timer for the splash screen.  Because this is a local
  ## # # function, when the splash screen no longer active, this timer will
  ## # # # no longer be active
  def splashTimerFired():
    delay = canvas.data["splashDelay"]
    canvas.delete(ALL)

    # call functions in an order such that the ball is in front of the
    # # background, but behind the text and buttons
    if canvas.data["splashScreen"]:
      # background and ball
      splashScreenBackGround();
      ball();
      splashScreenText();
      splashScreenButtons();

      # keep the timer running
      if delay != 0:
        canvas.after(delay, splashTimerFired);

  # get things rolling
  splashTimerFired();

##### END SPLASH SCREEN #####
#############################

"""
This next seciont of cold is responsible for drawing the game background
and the pause screen that occurs between every level and lost life
"""

############################################
##### DRAW BACKGROUND AND PAUSE SCREEN #####

## DRAW game background: takes "canvas", returns None
## # this draws a black background and a and white square over it, effectively
## # # giving the gamea border. Also, it draws the number of lives, and the
## # # # number of points earned over top of the black part of the border
def drawGameBackgound(canvas):
  # extract information from the canvas
  # # text
  fontSize = canvas.data["S_TEXT_SIZE"]
  level = canvas.data["currentTextLevel"]
  
  # # canvas
  CANVAS_WIDTH = canvas.data["CANVAS_WIDTH"]
  CANVAS_HEIGHT  = canvas.data["CANVAS_HEIGHT"]
  outsideMargin = canvas.data["outsideMargin"]

  # # gameplay
  difficulty = canvas.data["difficulty"]


  # compute / initialize variables
  # # text
  
  # # canvas
  outsideMargin = outsideMargin * .75
  oneQuarterX = CANVAS_WIDTH // 4
  threeQuartersX = CANVAS_WIDTH * .75
  centerX = CANVAS_WIDTH // 2
  centerY = CANVAS_HEIGHT // 2
  centerTopMargin = (outsideMargin / 1.5)
  centerBottomMargin = CANVAS_HEIGHT - (outsideMargin // 3)
  centerLeftMargin = outsideMargin // 2
  centerRightMargin = CANVAS_WIDTH - (outsideMargin // 3)

  # draw background
  canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill = "black")
  
  canvas.create_rectangle(outsideMargin, outsideMargin,
                         CANVAS_WIDTH - outsideMargin,
                         CANVAS_HEIGHT - outsideMargin,
                         fill = "white")

  canvas.create_rectangle(0, 0, outsideMargin, outsideMargin,
                          fill = "white")

  # draw header
  canvas.create_text(oneQuarterX, centerTopMargin,
                     text = "Lives: " + str(canvas.data["lives"]),
                     font = ("Courier", fontSize), fill = "white")
  canvas.create_text(centerX, centerTopMargin,
                     text = "Points: " + str(canvas.data["points"]),
                     font = ("Courier", fontSize), fill = "white")
  canvas.create_text(threeQuartersX, centerTopMargin,
                     text = level,
                     font = ("Courier", fontSize), fill = "white")    
                      
## DRAW paused screen: takes "canvas", returns None
## # this function draws a paused screen that occurs often throughout the
## # # the play of the game.
def drawPausedScreen(canvas):
  # extract information from the canvas
  # # text
  XL_TEXT_SIZE = canvas.data["XL_TEXT_SIZE"]
  L_TEXT_SIZE = canvas.data["L_TEXT_SIZE"]
  
  # # canvas
  CANVAS_WIDTH = canvas.data["CANVAS_WIDTH"];
  CANVAS_HEIGHT  = canvas.data["CANVAS_HEIGHT"];
  X_CENTER  = CANVAS_WIDTH // 2;
  X_1_THIRD = CANVAS_WIDTH * 0.33;
  X_2_THIRD = CANVAS_WIDTH * 0.66;
  Y_CENTER  = CANVAS_HEIGHT // 2;
  Y_1_THIRD = CANVAS_HEIGHT * 0.33;
  Y_2_THIRD = CANVAS_HEIGHT * 0.66;

  # compute / initialize variables
  canvas.data["pausedCounter"] += 1

  if(canvas.data["pausedCounter"] < 30):
    COLOR1 = "black";
    COLOR2 = "grey";
    COLOR3 = "grey";
  elif(canvas.data["pausedCounter"] < 60):
    COLOR1 = "grey";
    COLOR2 = "black";
    COLOR3 = "grey";
  elif(canvas.data["pausedCounter"] < 90):
    COLOR1 = "grey";
    COLOR2 = "grey";
    COLOR3 = "black";
  else: 
    canvas.data["paused"] = False;
    canvas.data["pausedCounter"] = 0;
    COLOR1 = "grey";
    COLOR2 = "grey";
    COLOR3 = "grey";

  # print the level
  canvas.create_text(X_CENTER, Y_1_THIRD, text = canvas.data["currentTextLevel"],
                     font = ("Courier", XL_TEXT_SIZE));

  canvas.create_text(X_CENTER, Y_CENTER, text = "Starting in...",
                     font = ("Courier", L_TEXT_SIZE));

  canvas.create_text(X_1_THIRD, Y_2_THIRD, text = "3",
                     font = ("Courier", XL_TEXT_SIZE), fill = COLOR1);  

  canvas.create_text(X_CENTER, Y_2_THIRD, text = "2",
                     font = ("Courier", XL_TEXT_SIZE), fill = COLOR2);

  canvas.create_text(X_2_THIRD, Y_2_THIRD, text = "1",
                     font = ("Courier", XL_TEXT_SIZE), fill = COLOR3);
    
##### END DRAW BACKGROUND AND PAUSE SCREEN #####
################################################

"""
The next block of code deals entirely with the paddles and their movment.
"""

#############################
##### DRAW MOVING PADDLE #####

## DRAW horizontal moving paddles: takes "canvas", returns None
## # this function draws the horizontal moving paddles overtop of the
## # # white part of the backgound
def drawHorizontalMovingPaddles(canvas):
  # extract information from the dictionary
  # # paddle
  paddleHeight = canvas.data["paddleHeight"]
  paddleWidth = canvas.data["paddleWidth"]
  horizontalCenterPaddle = canvas.data["horizontalCenterPaddle"]
  color = canvas.data["paddleColor"]
  borderWidth = canvas.data["borderWidth"]

  # # canvas
  outsideMargin = canvas.data["outsideMargin"]
  CANVAS_HEIGHT = canvas.data["CANVAS_HEIGHT"]

  # draw paddle at the bottom of the screen
  canvas.create_rectangle(horizontalCenterPaddle - paddleWidth,
                          CANVAS_HEIGHT - paddleHeight - outsideMargin,
                          horizontalCenterPaddle + paddleWidth,
                          CANVAS_HEIGHT - outsideMargin,
                          fill = color, width = borderWidth)
  
  # draw paddle at the top of the screen
  canvas.create_rectangle(horizontalCenterPaddle - paddleWidth, outsideMargin,
                          horizontalCenterPaddle + paddleWidth,
                          outsideMargin + paddleHeight,
                          fill = color, width = borderWidth)

## DRAW vertical moving paddles: takes "canvas", returns None
## # this function draws the vertical moving paddles overtop of the
## # # white part of the background
def drawVerticalMovingPaddles(canvas):

    # extract information from the canvas
    # # paddle
    paddleHeight = canvas.data["paddleHeight"]
    paddleWidth = canvas.data["paddleWidth"]
    outsideMargin = canvas.data["outsideMargin"]
    verticalCenterPaddle = canvas.data["verticalCenterPaddle"]
    color = canvas.data["paddleColor"]
    borderWidth = canvas.data["borderWidth"]
    
    # # canvas
    CANVAS_WIDTH = canvas.data["CANVAS_WIDTH"]


    # draw paddle on the left
    canvas.create_rectangle(outsideMargin,
                            verticalCenterPaddle - paddleWidth,
                            outsideMargin + paddleHeight,
                            verticalCenterPaddle + paddleWidth,
                            fill = color, width = borderWidth)

    # draw paddle on the right
    canvas.create_rectangle(CANVAS_WIDTH - outsideMargin - paddleHeight,
                            verticalCenterPaddle - paddleWidth,
                            CANVAS_WIDTH - outsideMargin,
                            verticalCenterPaddle + paddleWidth,
                            fill = color, width = borderWidth)
    
## MOVE the paddles: takes "canvas", returns None
## # this function is responsible for handling the movement of the paddles.
## # # It deals with special cases, such as the paddle moving too far to the
## # # # left, right, up, or down.
def movePaddles(canvas):

    # extract information from the dictionary
    # # paddle
    horizontalCenterPaddle = canvas.data["horizontalCenterPaddle"]
    verticalCenterPaddle = canvas.data["verticalCenterPaddle"]
    paddleWidth = canvas.data["paddleWidth"]
    paddleHeight = canvas.data["paddleHeight"]

    # # canvas
    CANVAS_HEIGHT = canvas.data["CANVAS_HEIGHT"]
    CANVAS_WIDTH = canvas.data["CANVAS_WIDTH"]
    outsideMargin = canvas.data["outsideMargin"]

    # moves the horizontal pads (the top and the bottom ones)
    def moveHorizontalPaddles():

        # if the pad isn't all the way to the left or right, let it move
        if (horizontalCenterPaddle + paddleWidth + outsideMargin + (paddleHeight // 2) <= CANVAS_WIDTH) and \
           (horizontalCenterPaddle - paddleWidth - outsideMargin - (paddleHeight // 2) >= 0):
           
            canvas.data["horizontalCenterPaddle"] += canvas.data["horizontalPaddleVelocity"]    

        # don't let the pad move if it's all the way to the right 
        elif horizontalCenterPaddle + paddleWidth + outsideMargin + (paddleHeight // 2) > CANVAS_WIDTH:
            canvas.data["horizontalCenterPaddle"] = CANVAS_WIDTH - paddleWidth - outsideMargin - paddleHeight
            canvas.data["horizontalPaddleVelocity"] = 0

        # don't let the pad move if it's all the way to the left
        elif horizontalCenterPaddle - paddleWidth - outsideMargin - (paddleHeight // 2) < 0:
            canvas.data["horizontalCenterPaddle"] = paddleWidth + outsideMargin + paddleHeight
            canvas.data["horizontalPaddleVelocity"] = 0

    # moves the vertical pads (left and right ones)
    def moveVerticalPaddles():

        # if the pad isn't all the way to the top or the bottom, let it move
        if (verticalCenterPaddle - paddleWidth - outsideMargin - (paddleHeight // 2) >= 0) and \
           (verticalCenterPaddle + paddleWidth + outsideMargin + (paddleHeight // 2) <= CANVAS_HEIGHT):

            canvas.data["verticalCenterPaddle"] += canvas.data["verticalPaddleVelocity"]

        # if the pad is at the top, don't let it move
        elif verticalCenterPaddle - paddleWidth - outsideMargin - (paddleHeight // 2) < 0:
            canvas.data["verticalCenterPaddle"] = paddleWidth + outsideMargin + paddleHeight
            canvas.data["verticalPaddleVelocity"] = 0

        # if the pad is at the bottom, don't let it move
        elif verticalCenterPaddle + paddleWidth + outsideMargin + (paddleHeight // 2) > CANVAS_HEIGHT:
            canvas.data["verticalCenterPaddle"] = CANVAS_HEIGHT - paddleWidth - outsideMargin - paddleHeight
            canvas.data["verticalPaddleVelocity"] = 0

    # call local functions
    moveHorizontalPaddles()
    moveVerticalPaddles()
               
##### END DRAW MOVING PADDLES #####
#################################
    
"""
The next block of code deals entirely with the ball and its movment.
"""

############################
##### DRAW MOVING BALL #####
    
## DRAW ball: takes "canvas", returns None
## # this function draws the ball over top of the white part of the
## # # game background. The color of the ball changes everytime it
## # # # it hits a paddle. The color sequence is a pattern
def drawBall(canvas):

    # extract information from the canvas
    # # ball
    ballColorNumber = canvas.data["ballColorCounter"]
    ballCenterX = canvas.data["ballCenterX"]
    ballCenterY = canvas.data["ballCenterY"]
    radius = canvas.data["radius"]
    borderWidth = canvas.data["borderWidth"]

    # see if the ball has contacted a block
    ballContactsBlock(canvas)
    
    # determine color
    if ballColorNumber % 5 == 0:
        color = "red"
    if ballColorNumber % 5 == 1:
        color = "orange"
    if ballColorNumber % 5 == 2:
        color = "green"
    if ballColorNumber % 5 == 3:
        color = "blue"
    if ballColorNumber % 5 == 4:
        color = "purple"

    # draw ball
    canvas.create_oval(ballCenterX - radius, ballCenterY - radius,
                       ballCenterX + radius, ballCenterY + radius,
                       fill = color, width = borderWidth)


## DETERMINE the downward movment of the ball: takes "canvas", returns None
## # this function handles the special cases of the ball as it moves downward.
## # # the most important purpose of this fuction is to make sure it bounces
## # # # off of a paddle
def ballPositiveYVelocity(canvas):

    # extract information from the dictionary
    # # ball
    ballCenterY = canvas.data["ballCenterY"]
    ballCenterX = canvas.data["ballCenterX"]
    radius = canvas.data["radius"]
    ballVelocityY = canvas.data["ballVelocityY"]

    # # paddle
    paddleHeight = canvas.data["paddleHeight"]
    outsideMargin = canvas.data["outsideMargin"]
    horizontalCenterPaddle = canvas.data["horizontalCenterPaddle"]
    paddleWidth = canvas.data["paddleWidth"]
    minPaddleWidth = canvas.data["CANVAS_WIDTH"] // 7

    # # canvas
    CANVAS_HEIGHT = canvas.data["CANVAS_HEIGHT"]

    # # gameplay
    pointsPerHit = canvas.data["pointsPerHit"]

    
    # ball above the bottom pad
    if ballCenterY < (CANVAS_HEIGHT - radius - paddleHeight - outsideMargin):

        canvas.data["ballCenterY"] += ballVelocityY

    # ball at/below the bottom pad
    elif ballCenterY >= (CANVAS_HEIGHT - radius - paddleHeight - outsideMargin):
        # pad below the ball?
        if (horizontalCenterPaddle - paddleWidth) <= ballCenterX <= (horizontalCenterPaddle + paddleWidth): 
            canvas.data["ballVelocityY"] -= (ballVelocityY * 2)
            canvas.data["points"] += pointsPerHit
            canvas.data["ballColorCounter"] += 1

            # determine the x direction of the ball (based on where it hits)
            ballXDirectionDeterminate(canvas)
            
        # pad not below the ball
        elif ballCenterY >= (CANVAS_HEIGHT - outsideMargin):
            canvas.data["lives"] -= 1
            if paddleWidth > minPaddleWidth: canvas.data["paddleWidth"] *= .9
            canvas.data["points"] -= 25
            canvas.data["turnOver"] = True

        # neither of the previous two
        else:
            canvas.data["ballCenterY"] += ballVelocityY
            
## DETERMINE the upward movment of the ball: takes "canvas", returns None
## # this function handles the special cases of the ball as it moves upward.
## # # the most important purpose of this fuction is to make sure it bounces
## # # # off of a paddle
def ballNegativeYVelocity(canvas):

    # extract information from the dictionary

    # # ball
    ballCenterY = canvas.data["ballCenterY"]
    ballCenterX = canvas.data["ballCenterX"]
    radius = canvas.data["radius"]
    ballVelocityY = canvas.data["ballVelocityY"]

    # # paddle
    outsideMargin = canvas.data["outsideMargin"]
    horizontalCenterPaddle = canvas.data["horizontalCenterPaddle"]
    paddleWidth = canvas.data["paddleWidth"]
    paddleHeight = canvas.data["paddleHeight"]
    minPaddleWidth = canvas.data["CANVAS_WIDTH"] // 7
    
    # # canvas
    CANVAS_HEIGHT = canvas.data["CANVAS_HEIGHT"]

    # gameplay
    pointsPerHit = canvas.data["pointsPerHit"]
    
    # ball below the top pad
    if ballCenterY > (radius + paddleHeight + outsideMargin):                       
        canvas.data["ballCenterY"] += ballVelocityY

    # ball at/above the top pad
    if ballCenterY <= (radius + paddleHeight + outsideMargin):

        # pad above the ball
        if (horizontalCenterPaddle - paddleWidth) < ballCenterX < (horizontalCenterPaddle + paddleWidth):
            canvas.data["ballVelocityY"] = abs(ballVelocityY)
            canvas.data["points"] += pointsPerHit
            canvas.data["ballColorCounter"] += 1

        # pad not above the ball
        elif ballCenterY <= outsideMargin:
            canvas.data["turnOver"] = True
            if paddleWidth > minPaddleWidth: canvas.data["paddleWidth"] *= .9
            canvas.data["lives"] -= 1
            canvas.data["points"] -= 25

        # neither of the previous two
        else:
            canvas.data["ballCenterY"] += ballVelocityY
            
## DETERMINE the right movment of the ball: takes "canvas", returns None
## # this function handles the special cases of the ball as it moves right.
## # # the most important purpose of this fuction is to make sure it bounces
## # # # off of a paddle
def ballPositiveXVelocity(canvas):

    # extract information from the dictionary
    # # ball
    ballCenterY = canvas.data["ballCenterY"]
    ballCenterX = canvas.data["ballCenterX"]
    radius = canvas.data["radius"]
    ballVelocityX = canvas.data["ballVelocityX"]

    # # paddle
    paddleHeight = canvas.data["paddleHeight"]
    outsideMargin = canvas.data["outsideMargin"]
    verticalCenterPaddle = canvas.data["verticalCenterPaddle"]
    paddleWidth = canvas.data["paddleWidth"]
    minPaddleWidth = canvas.data["CANVAS_WIDTH"] // 7
    # # canvas
    CANVAS_WIDTH = canvas.data["CANVAS_WIDTH"]    

    # gameplay
    pointsPerHit = canvas.data["pointsPerHit"]

    # ball to the left of the right pad
    if ballCenterX < (CANVAS_WIDTH - radius - paddleHeight - outsideMargin):
        canvas.data["ballCenterX"] += ballVelocityX

    # ball at/to the right of the right pad
    if ballCenterX >= (CANVAS_WIDTH - radius - paddleHeight - outsideMargin):

        # pad to the right of the ball?
        if (verticalCenterPaddle - paddleWidth) < ballCenterY < (verticalCenterPaddle + paddleWidth):
            canvas.data["ballVelocityX"] -= (ballVelocityX*2)
            canvas.data["points"] += pointsPerHit
            canvas.data["ballColorCounter"] += 1

        # pad not to the right of the ball
        elif ballCenterX >= CANVAS_WIDTH - outsideMargin:
            canvas.data["turnOver"] = True
            if paddleWidth > minPaddleWidth: canvas.data["paddleWidth"] *= .9
            canvas.data["lives"] -= 1
            canvas.data["points"] -= 25

        # neither of the previous two
        else:
            canvas.data["ballCenterX"] += ballVelocityX

## DETERMINE the left movment of the ball: takes "canvas", returns None
## # this function handles the special cases of the ball as it moves left.
## # # the most important purpose of this fuction is to make sure it bounces
## # # # off of a paddle
def ballNegativeXVelocity(canvas):

    # extract information from the canvas
    # # ball
    ballCenterY = canvas.data["ballCenterY"]
    ballCenterX = canvas.data["ballCenterX"]
    radius = canvas.data["radius"]
    ballVelocityX = canvas.data["ballVelocityX"]

    # # paddle
    paddleHeight = canvas.data["paddleHeight"]
    outsideMargin = canvas.data["outsideMargin"]
    verticalCenterPaddle = canvas.data["verticalCenterPaddle"]
    paddleWidth = canvas.data["paddleWidth"]
    minPaddleWidth = canvas.data["CANVAS_WIDTH"] // 7
    
    # # canvas
    CANVAS_WIDTH = canvas.data["CANVAS_WIDTH"]    

    # # gameplay
    pointsPerHit = canvas.data["pointsPerHit"]
   
    # ball to the right of the left pad
    if ballCenterX > (radius + paddleHeight + outsideMargin):
        canvas.data["ballCenterX"] += ballVelocityX

    # ball at/to the left of the left pad
    if ballCenterX <= (radius + paddleHeight + outsideMargin):

        # pad to the left of the ball?
        if (verticalCenterPaddle - paddleWidth) < ballCenterY < (verticalCenterPaddle + paddleWidth):
            canvas.data["ballVelocityX"] = abs(ballVelocityX)
            canvas.data["points"] += pointsPerHit
            canvas.data["ballColorCounter"] += 1

        # pad not to the left of the ball
        elif ballCenterX <= outsideMargin:
            canvas.data["turnOver"] = True
            if paddleWidth > minPaddleWidth: canvas.data["paddleWidth"] *= .9
            canvas.data["lives"] -= 1
            canvas.data["points"] -= 25

        # neither of the previous
        else:
            canvas.data["ballCenterX"] += ballVelocityX

## DETERMINE the x velocity of the ball: takes "canvas", returns None
## # this function determines the x velocity of the ball as well as the color
## # # of the pads.  This all depends on where the ball hits the BOTTOM pad.
## # # # all the pads will follow the color of the bottom pad. Again, only the
## # # # # bottom pad determines velocity.
def ballXDirectionDeterminate(canvas):

    # compute / initialize variables
    # # ball
    velocityFactor = 0
    ballCenterX = canvas.data["ballCenterX"]
    
    # # paddle
    paddleFactor = canvas.data["paddleWidth"] // 6.0
    horizontalCenterPaddle = canvas.data["horizontalCenterPaddle"]

    # ball at the middle of the paddles
    if ballCenterX == horizontalCenterPaddle:

        # set color/velocity factor
        canvas.data["paddleColor"] = "white"
        velocityFactor = 0

        # extra points, this is REALLY hard
        canvas.data["points"] += 100

    # ball to the left of the cetner of the paddle
    elif ballCenterX < horizontalCenterPaddle:

        # compute the velocity factor
        velocityFactor = (horizontalCenterPaddle - ballCenterX) // 100.0

        # set color correctly
        if ballCenterX < (horizontalCenterPaddle): canvas.data["paddleColor"] = "black"
        if ballCenterX < (horizontalCenterPaddle - paddleFactor): canvas.data["paddleColor"] = "purple"
        if ballCenterX < (horizontalCenterPaddle - (paddleFactor * 2)): canvas.data["paddleColor"] = "blue"
        if ballCenterX < (horizontalCenterPaddle - (paddleFactor * 3)): canvas.data["paddleColor"] = "green"
        if ballCenterX < (horizontalCenterPaddle - (paddleFactor * 4)): canvas.data["paddleColor"] = "yellow"
        if ballCenterX < (horizontalCenterPaddle - (paddleFactor * 5)): canvas.data["paddleColor"] = "red"

        # reset velocity
        canvas.data["ballVelocityX"] = (canvas.data["ballVelocityY"] * velocityFactor)

    # ball to the right of the center of paddle
    elif ballCenterX > horizontalCenterPaddle:

        # compute a velocity factor
        velocityFactor = (ballCenterX - horizontalCenterPaddle) // 100.0

        # set colors correctly
        if ballCenterX > horizontalCenterPaddle: canvas.data["paddleColor"] = "black"
        if ballCenterX > (horizontalCenterPaddle + paddleFactor): canvas.data["paddleColor"] = "purple"
        if ballCenterX > (horizontalCenterPaddle + (paddleFactor * 2)): canvas.data["paddleColor"] = "blue"
        if ballCenterX > (horizontalCenterPaddle + (paddleFactor * 3)): canvas.data["paddleColor"] = "green"
        if ballCenterX > (horizontalCenterPaddle + (paddleFactor * 4)): canvas.data["paddleColor"] = "yellow"
        if ballCenterX > (horizontalCenterPaddle + (paddleFactor * 5)): canvas.data["paddleColor"] = "red"

        # reset velocity
        canvas.data["ballVelocityX"] = -(canvas.data["ballVelocityY"] * velocityFactor)

    ballNegativeXVelocity(canvas)

##### END DRAW MOVING BALL #####
################################

"""
The next block of code has to do with the blocks that need breaking.
"""

##################
##### BLOCKS #####

## DRAW blocks: takes "canvas", returns None
## # this function draws the blocks
def drawBlocks(canvas):

    # extract information from the canvas
    # # grid
    blockGrid = canvas.data["currentBlockGrid"]
    colorGrid = canvas.data["currentColorGrid"]
    blockRows = canvas.data["rows"]
    blockColumns = canvas.data["columns"]
    rowStep = canvas.data["rowStep"]
    columnStep = canvas.data["columnStep"]
    borderWidth = canvas.data["borderWidth"]


    # iterate over all of the rows/columns to draw all of the blocks
    for column in range(blockColumns):
        for row in range(blockRows):
            if blockGrid[row][column]:

                color = colorGrid[row][column]

                canvas.create_rectangle(column * columnStep, row * rowStep,
                                        column * columnStep + columnStep,
                                        row * rowStep + rowStep,
                                        fill = color,
                                        width = borderWidth)
                
## CONTACT the blocks: takes "canvas", returns None
## # this function determines if the ball contacts the blocks or not,
## # # deletes the blocks that are hit, and then changes the direction
## # # # of the ball according to how it hit
def ballContactsBlock(canvas):

    # extract information from the dictionary
    # # ball
    ballCenterX = canvas.data["ballCenterX"]
    ballCenterY = canvas.data["ballCenterY"]
    ballVelocityY = canvas.data["ballVelocityY"]
    ballVelocityX = canvas.data["ballVelocityX"]
    ballCenterX = canvas.data["ballCenterX"]
    ballCenterY = canvas.data["ballCenterY"]
    radius = canvas.data["radius"]

    # # canvas
    CANVAS_WIDTH = canvas.data["CANVAS_WIDTH"]

    # # paddle
    paddleWidth = canvas.data["paddleWidth"]

    # # grid
    rowStep = canvas.data["rowStep"]
    columnStep = canvas.data["columnStep"]
    blockGrid = canvas.data["currentBlockGrid"]
    colorGrid = canvas.data["currentColorGrid"]
    blankLevel = canvas.data["blankLevel"]
    
    # # canvas
    CANVAS_WIDTH = canvas.data["CANVAS_WIDTH"]
    # # paddle
    paddlWidth = canvas.data["paddleWidth"]

    # compute variabels
    maxPaddleWidth = CANVAS_WIDTH // 4
    minPaddleWidth = CANVAS_WIDTH // 7


    ## POWERUPS/BREAK blocks: takes row and column, returns None
    ## # this local function adjusts variables as needed based on whether
    ## # # or not a power up/block was broken
    def breakBlockPowerUp(row, column):
        
        # remove the block
        canvas.data["currentBlockGrid"][row][column] = False

        # add to the points
        canvas.data["points"] += 5
        
        # smaller paddle
        if colorGrid[row][column] == "red" and paddleWidth > minPaddleWidth:
            canvas.data["paddleWidth"] *= .9

        # larger paddle
        elif colorGrid[row][column] == "green" and paddleWidth < maxPaddleWidth:
            canvas.data["paddleWidth"] *= 1.1

        # extra life
        elif colorGrid[row][column] == "white":
            canvas.data["lives"] += 1
            
    # ball moving up
    if ballVelocityY < 0:

        # determine row and column the ball is in
        row = int(((ballCenterY) - radius) // rowStep)
        column = int(ballCenterX // columnStep)

        # test for a block, and readjust variables
        if blockGrid[row][column]:

            # reverse direction
            canvas.data["ballVelocityY"] *= -1

            # check for powerups/break blocks
            breakBlockPowerUp(row, column)

            return   

    # ball moving down
    elif ballVelocityY > 0:
        
        # determine row and column the ball is in
        row = int(((ballCenterY) + radius) // rowStep)
        column = int(ballCenterX // columnStep)

        # test for a block, and readjust vaiables
        if blockGrid[row][column]:

            # reverse the direction
            canvas.data["ballVelocityY"] *= -1

            # check for powerups/break blocks
            breakBlockPowerUp(row, column)

            return
       
    # ball moving left or straight up and down
    if ballVelocityX < 0 or ballVelocityX == 0:
        
        # determine row and column the ball is in
        row = int(ballCenterY // rowStep)
        column = int(((ballCenterX) - radius) // columnStep)

        # test for a block, and readjust vaiables
        if blockGrid[row][column]:
            
            # reverse direction
            canvas.data["ballVelocityX"] *= -1

            # check powerups/ break blocks
            breakBlockPowerUp(row, column)

            return # return out before bad things happen

        # reset the column. this will only trip used in very specific cases when
        # # when half or less of the ball is in a given column
        column = int(((ballCenterX) + radius) // columnStep)

        # test for a block, and readjust variables
        if blockGrid[row][column]:

            # reverse direction
            canvas.data["ballVelocityY"] *= -1

            # check for powerups/break blocks
            breakBlockPowerUp(row, column)

            return # return out before bad things happen

    # ball moving right or straight up and down
    elif ballVelocityX > 0 or ballVelocityX == 0:
        # determine row and column the ball is in
        row = (ballCenterY // rowStep)
        column = int(((ballCenterX) + radius) // columnStep)

        # test for a block, and readjust vaiables
        if blockGrid[row][column]:

            # reverse the direction
            canvas.data["ballVelocityX"] *= -1

            # check for powerups/break blocks
            breakBlockPowerUp(row, column)

            return # return out before bad things happen

        # reset the column. this will only trip used in very specific cases when
        # # when half or less of the ball is in a given column
        column = int(((ballCenterX) - radius) / columnStep)

        # test for a block, and readjust variables
        if blockGrid[row][column]:

            # reverse direction
            canvas.data["ballVelocityY"] *= -1

            # check for powerups/break blocks
            breakBlockPowerUp(row, column)

            return # return out before bad things happen

    # see if the level needs to be advanced
    advanceLevel(canvas)



##### END BLOCKS #####
######################

"""
The next block of code is the the control center of the program.
It advances the levels, determins if someone is a winner, draws
everything on the canvas, handles all of the mouse presses, handles
all of the key presses, initializes the dicitionary, resets the
game between lives and games, and handles all of the AI.
This section of the code is about
one third of the code total, so it is pretty significant.
"""

###########################
##### CONTROL CENTER ######

## CONGRADULATE a winner: takes "canvas", returns None
def winner(canvas):

    # extract information from the dictionary
    XL_TEXT_SIZE = canvas.data["XL_TEXT_SIZE"]

    # compute/initialize variables
    centerX = canvas.data["CANVAS_WIDTH"] // 2
    centerY = canvas.data["CANVAS_HEIGHT"] // 2

    # blinks "WINNER" a few times while the score is increased 1000 points
    # # for winning
    if canvas.data["delayCounter"] < 200:
        canvas.data["delayCounter"] += 1

        if canvas.data["delayCounter"] % 36 < 18:
            canvas.create_text(centerX, centerY,
                               text = "WINNER",
                               font = ("Courier", XL_TEXT_SIZE))
        canvas.data["points"] += 5

    # this keeps blinking "WINNER" while adding 100 points for ever life
    # # retained in the course of winning
    elif canvas.data["lives"] > 0:
        
        canvas.data["delayCounter"] += 1
        if canvas.data["delayCounter"] % 36 < 18:
            canvas.create_text(centerX, centerY,
                               text = "WINNER",
                               font = ("Courier", XL_TEXT_SIZE))
            
        if canvas.data["delayCounter"] % 36 == 18:
            canvas.data["paddleWidth"] *= .9
            canvas.data["lives"] -= 1
            canvas.data["points"] += 100
            
    # once all of the points have been awarded, turn the duties over to the
    # # turnOver fuction
    else:
        turnOver(canvas)

## ADVANCE level: takes "canvas", returns None
## # this function advances the level or determines if the player has won
def advanceLevel(canvas):

    # initialize variabes
    blankLevel = canvas.data["blankLevel"]
    maxPaddleWidth = canvas.data["CANVAS_WIDTH"] // 4

    # if the level is blank, readjust variables as needed to go to the next level
    if blankLevel == canvas.data["currentBlockGrid"] and len(canvas.data["keyLevelList"]) > 0:

        reset(canvas)
        canvas.data["paused"] = True
        canvas.data["lives"] += 1

        if canvas.data["paddleWidth"] < maxPaddleWidth: canvas.data["paddleWidth"] *= 1.1

        canvas.data["points"] += 100

        levelKey = canvas.data["keyLevelList"].pop()
        
        canvas.data["currentBlockGrid"] = canvas.data[levelKey]
        canvas.data["currentColorGrid"] = canvas.data[levelKey+"ColorGrid"]
        canvas.data["currentTextLevel"] = canvas.data["textLevelList"].pop()

    # maybe someone has won?
    elif blankLevel == canvas.data["currentBlockGrid"] and len(canvas.data["keyLevelList"]) == 0:

        canvas.data["winner"] = True
        
## REDRAW all: takes "canvas", returns None
## # this function draws everything on the canvas with A LOT of help
## # # from helper functions. It makes sure the correct functions are
## # # # called.        
def redrawAll(canvas):
    # initialize variabes
    paused = canvas.data["paused"]
    
    # if the splash screen is up, make sure tha splash screen is called
    if canvas.data["splashScreen"]:
        splashScreen(canvas)

    # if the game is being played, call the gameplay functions
    else:
        canvas.delete(ALL)
 
        drawGameBackgound(canvas)
        drawHorizontalMovingPaddles(canvas)
        drawVerticalMovingPaddles(canvas)
        drawBlocks(canvas)
        drawBall(canvas)

        # life lost / game over?
        if canvas.data["turnOver"]:
            turnOver(canvas)
    # winner ?
    if canvas.data["winner"]:  
        winner(canvas)

    # paused ?
    elif paused:
        drawPausedScreen(canvas)

## PLAY the game: takes "cavnas", returns None
## # this function changes the values of the variables that need to be
## # # changed in order to go from the splash screen to the game
def getGameReady(canvas):
  canvas.data["splashDelay"] = 0
  canvas.data["delayCounter"] = 0
  canvas.data["pausedCounter"] = 0
  canvas.data["ballCenterX"] = canvas.data["CANVAS_WIDTH"] // 2
  canvas.data["ballCenterY"] = canvas.data["CANVAS_HEIGHT"] // 2
  canvas.data["splashScreen"] = False;
  canvas.data["playGameScreen"] = True;
  canvas.data["winner"] = False;
  canvas.data["paused"] = True;

## CLICK the splash screen: takes "canvas" and "event", returns None
## # this function deals with all of the events that have to do with the
## # # splash screen.  It takes you thdef splashScreenClickrough the menus of the splash screen,
## # # # changes the color of the background when it is clicked and speeds
## # # # # up the ball whenever the creator's name is clicked.
def splashScreenClick(canvas, event):
  # extract information from the canvas
  # # button
  buttonSize = canvas.data["BUTTON_X_SIZE"]
  buttonMargin = canvas.data["BUTTON_MARGIN"]

  CANVAS_WIDTH = canvas.data["CANVAS_WIDTH"]

  Y_LOC_TOP_BUTTON    = canvas.data["Y_LOC_TOP_BUTTON"];
  Y_LOC_BOTTOM_BUTTON = canvas.data["Y_LOC_BOTTOM_BUTTON"];
  BUTTON_X_SIZE = canvas.data["BUTTON_X_SIZE"];
  BUTTON_Y_SIZE = canvas.data["BUTTON_Y_SIZE"];
  BUTTON_MARGIN = canvas.data["BUTTON_MARGIN"];
  X_CENTER = CANVAS_WIDTH // 2;

  # # canvas
  CANVAS_HEIGHT = canvas.data["CANVAS_HEIGHT"]
  CANVAS_WIDTH = canvas.data["CANVAS_WIDTH"]

  # # highscores

  # compute and initialize variables
  clickButtonSize = buttonSize - buttonMargin
  marginX = CANVAS_WIDTH // 20
  marginY = CANVAS_HEIGHT // 20
  centerX = CANVAS_WIDTH // 2

  if (((X_CENTER - BUTTON_X_SIZE + BUTTON_MARGIN) < event.x < (X_CENTER + BUTTON_X_SIZE - BUTTON_MARGIN)) and 
      ((Y_LOC_TOP_BUTTON - BUTTON_Y_SIZE + BUTTON_MARGIN) < event.y < (Y_LOC_TOP_BUTTON + BUTTON_Y_SIZE - BUTTON_MARGIN))):
    getGameReady(canvas)
    canvas.data["difficulty"] = "easy";
    canvas.data["pointsPerHit"] = 1;
    canvas.data["ballVelocityY"] = canvas.data["CANVAS_WIDTH"] // 85;
    timerFired(canvas)

  elif (((X_CENTER - BUTTON_X_SIZE + BUTTON_MARGIN) < event.x < (X_CENTER + BUTTON_X_SIZE - BUTTON_MARGIN)) and 
      ((Y_LOC_BOTTOM_BUTTON - BUTTON_Y_SIZE + BUTTON_MARGIN) < event.y < (Y_LOC_BOTTOM_BUTTON + BUTTON_Y_SIZE - BUTTON_MARGIN))):
    print ("Goodbye");

## MOUSE pressed: takes "event", returns None
## # this function deals with all the events that happen when the mouse
## # # is pressed
def mousePressed(event):
  # initialize variables
  canvas = event.widget.canvas

  # if the splashscreen is up, call helper function
  if canvas.data["splashScreen"]: 
    splashScreenClick(canvas, event);
    
## KEY pressed: takes "event", returns None
## # this function deals with all of the events taht happen when the keyboard
## # # is pressed
def keyPressed(event):
  # initialize variable
  canvas = event.widget.canvas

  # extract information from the canvas
  CANVAS_WIDTH = canvas.data["CANVAS_WIDTH"]
  turnOver = canvas.data["turnOver"]
  paused = canvas.data["paused"]
  splashScreen = canvas.data["splashScreen"]
  win = canvas.data["winner"]
  gameOverScreen = canvas.data["gameOverScreen"]

  # if the AI is not in control, go ahead and allow the user to type
  # go to a helper funtion if it's the gameOverScreen. This is where the
  # # user types his/her name
  if canvas.data["gameOverScreen"] == True:
    typeName(canvas, event)
  
  else: 
    # moves top and bottom paddles to the left
    if event.keysym == "Left" and not turnOver:
        canvas.data["horizontalPaddleVelocity"] = CANVAS_WIDTH // 70
        canvas.data["horizontalPaddleVelocity"] -= (canvas.data["horizontalPaddleVelocity"] * 2)

    # moves top and bottom paddles to the right
    elif event.keysym == "Right" and not turnOver:
        canvas.data["horizontalPaddleVelocity"] = CANVAS_WIDTH // 70
        canvas.data["horizontalPaddleVelocity"] = abs(canvas.data["horizontalPaddleVelocity"])

    # moves left and rights paddles down
    elif event.keysym == "Down" and not turnOver:
        canvas.data["verticalPaddleVelocity"] = CANVAS_WIDTH // 70
        canvas.data["verticalPaddleVelocity"] = abs(canvas.data["verticalPaddleVelocity"])

    # moves left and right paddles up
    elif event.keysym == "Up" and not turnOver:
        canvas.data["verticalPaddleVelocity"] = CANVAS_WIDTH // 70
        canvas.data["verticalPaddleVelocity"] -= (canvas.data["verticalPaddleVelocity"] * 2)

    # stops the paddle from moving
    elif event.keysym == "space" and not turnOver:
        canvas.data["horizontalPaddleVelocity"] = 0
        canvas.data["verticalPaddleVelocity"] = 0

    # quits the game, goes back to the original splash screen
    elif event.keysym == "q" and not splashScreen:
        canvas.data["paused"] = False
        init(canvas)
        
    # pause the game
    elif event.keysym == "p":

        # if the game is paused, unpause
        if canvas.data["paused"]:
            canvas.data["paused"] = False
            
        # if the game is not paused, pause
        else:
            canvas.data["paused"] = True
            
    # unpause the game as prompted by the paused game screen
    if event.keysym == "space" and canvas.data["paused"]:
        canvas.data["paused"] = False


## INITIALIZES the dictionary: takes "canvas", returns None
## # this function uses local functions (for organization purposes) to
## # # initialize all of thevalues in the dictionary
def init(canvas):

  ## SPLASH SCREEN INFORMATION: takes nothing, returns None
  def splashInit():
    # buttons
    canvas.data["BUTTON_COLOR_ACTIVE"] = "white"
    canvas.data["BUTTON_COLOR_INACTIVE"] = "grey"
    canvas.data["BUTTON_X_SIZE"] = canvas.data["CANVAS_WIDTH"] // 10;
    canvas.data["BUTTON_Y_SIZE"] = canvas.data["CANVAS_HEIGHT"] // 20;
    canvas.data["BUTTON_MARGIN"] = canvas.data["BUTTON_X_SIZE"] - (canvas.data["CANVAS_WIDTH"] / 11)

    # ball
    canvas.data["splashBallColor"] = "white"
    canvas.data["SPLASH_RADIUS"] = canvas.data["CANVAS_WIDTH"] // 50
    canvas.data["splashBallVX"] = 0
    canvas.data["splashBallVY"] = canvas.data["CANVAS_WIDTH"] // 100

    # current screen
    canvas.data["splashScreen"] = True;
    canvas.data["playGameScreen"] = False;
    canvas.data["SPLASH_SCREEN_COLOR"] = "white"

    canvas.data["Y_LOC_TITLE"]          = 0.25*canvas.data["CANVAS_HEIGHT"];
    canvas.data["Y_LOC_AUTHOR1"]        = 0.45*canvas.data["CANVAS_HEIGHT"];
    canvas.data["Y_LOC_AUTHOR2"]        = 0.50*canvas.data["CANVAS_HEIGHT"];
    canvas.data["Y_LOC_TOP_BUTTON"]     = 0.70*canvas.data["CANVAS_HEIGHT"];
    canvas.data["Y_LOC_BOTTOM_BUTTON"]  = 0.85*canvas.data["CANVAS_HEIGHT"];
    # misc
    canvas.data["fastCounter"] = 0
    canvas.data["splashDelay"] = 15
    canvas.data["delayCounter"] = 0
    canvas.data["pausedCounter"] = 0
    canvas.data["name"] = "Type name please."

  ## UNIVERSAL INFORMATION: takes nothing, returns None,
  ## # but saves the information in the dictionary
  def universalInit():
    # ball
    canvas.data["ballCenterX"] = canvas.data["CANVAS_WIDTH"] // 2
    canvas.data["ballCenterY"] = canvas.data["CANVAS_HEIGHT"] // 2

    # all moving objects
    canvas.data["borderWidth"] = canvas.data["CANVAS_WIDTH"] // 350

    # text
    canvas.data["S_TEXT_SIZE"] = canvas.data["CANVAS_WIDTH"] // 35
    canvas.data["M_TEXT_SIZE"] = canvas.data["CANVAS_WIDTH"] // 28
    canvas.data["L_TEXT_SIZE"] = canvas.data["CANVAS_WIDTH"] // 20
    canvas.data["XL_TEXT_SIZE"] = canvas.data["CANVAS_WIDTH"] // 10

    # url / filename
    canvas.data["dateUrl"] = "http://tycho.usno.navy.mil/cgi-bin/timer.pl"
    canvas.data["highScoreFileName"] = "_high_scores.txt"
    
      
  ## GAMEPLAY INFORMATION: takes nothing, returns None,
  ## # but saves the information in the dictionary
  def gameInit():
    # paddles
    canvas.data["horizontalCenterPaddle"] = canvas.data["CANVAS_WIDTH"] / 2
    canvas.data["verticalCenterPaddle"] = canvas.data ["CANVAS_WIDTH"] / 2
    canvas.data["horizontalPaddleVelocity"] = 0
    canvas.data["verticalPaddleVelocity"] = 0
    canvas.data["paddleWidth"] = canvas.data["CANVAS_WIDTH"] / 6
    canvas.data["paddleHeight"] = canvas.data["CANVAS_WIDTH"] / 50
    canvas.data["paddleColor"] = "black"
    
    # ball
    canvas.data["radius"] = canvas.data["CANVAS_WIDTH"] / 60
    canvas.data["ballVelocityX"] = canvas.data["CANVAS_WIDTH"] / 400
    canvas.data["ballVelocityY"] = 0
    canvas.data["ballColorCounter"] = 0

    # general gameplay
    canvas.data["lives"] = 3
    canvas.data["points"] = 0
    canvas.data["turnOver"] = False
    canvas.data["delay"] = 30
    canvas.data["turnOverCounter"] = 0
    canvas.data["paused"] = False
    canvas.data["pointsPerHit"] = 0
    
    # misc
    canvas.data["outsideMargin"] = canvas.data["CANVAS_WIDTH"] / 20

  ## MAKE LEVELS: takes nothing, returns None,
  ## # but sets the levels in the dictionary
  def makeLevels():
    ## BLANK LEVEL: takes nothing, returns blank level's boolean/color grids
    ## # this function makes a blank level
    def makeBlankLevel():
      # exract information from the dictionary
      rows = canvas.data["rows"]
      columns = canvas.data["columns"]
      colors = ["red", "red", "white", "green", 
                "blue", "blue", "blue", "blue",
                "cyan", "cyan", "cyan", "cyan",
                "purple", "purple", "purple", "purple",
                "orange", "orange", "orange", "orange",
                "magenta", "magenta", "magenta", "magenta",
                "yellow", "yellow", "yellow", "yellow"]

      # initialize variables
      blockGrid = []
      colorGrid = []

      # set all values to False
      for row in range(rows):
        blockGrid += [[False] * columns]
        colorGrid += [[None] * columns]

      def getColor(row, column):
        while True:
          color = random.choice(colors)
          if ((color != colorGrid[row - 1][column]) and (color != colorGrid[row][column - 1])):
            return color
      # randomize the colors for all of the cells
      for row in range(1, rows - 1):
        for column in range(1, columns - 1):
          colorGrid[row][column] = getColor(row, column)
                    
      return (blockGrid, colorGrid)

    ## LEVEL ONE: takes nothing, returns level's boolean/color grids
    ## # this function makes level one
    def makeLevelOne():
        # initialize variables
        (blockGrid,colorGrid) = makeBlankLevel()

        # set certain blocks to True
        for row in range(5, 10):
            for column in range(1,4):
                blockGrid[row][column] = True

        return (blockGrid, colorGrid)

    ## LEVEL TWO: takes nothing, returns level's boolean/color grids
    ## # this function makes level two
    def makeLevelTwo():

        # initialize variables
        (blockGrid,colorGrid) = makeBlankLevel()

        # set certain blocks to True
        for row in range(3, 15):
            blockGrid[row][1] = True
                
        for row in range(3, 15):
            blockGrid[row][3] = True
                
        return (blockGrid, colorGrid)

    ## LEVEL THREE: takes nothing, returns level's boolean/color grids
    ## # this funciton makes level three
    def makeLevelThree():

        # initialize variables
        (blockGrid,colorGrid) = makeBlankLevel()

        # set certain blocks to True
        for row in range(3, 9):
            blockGrid[row][1] = True

        for row in range(3, 9):
            blockGrid[row][3] = True
                
        for row in range(13, 19):
            blockGrid[row][1] = True
            
        for row in range(13, 19):
            blockGrid[row][3] = True

        return (blockGrid, colorGrid)

    ## LEVEL FOUR: takes nothing, returns level's boolean/color grids
    ## # this function makes level four
    def makeLevelFour():

        # initialize variables
        (blockGrid,colorGrid) = makeBlankLevel()

        # set certain blocks to True
        for row in range(3, 17, 2):
            for column in range(1, 4, 2):
                blockGrid[row][column] = True
                
        for row in range(4, 16, 2):
            for column in range(2, 4, 2):
                blockGrid[row][column] = True

        return (blockGrid, colorGrid)

    ## LEVEL FIVE: takes nothing, returns level's boolean/color grids
    ## # this function makes level five
    def makeLevelFive():

        # initialize variables
        (blockGrid,colorGrid) = makeBlankLevel()

        # set certain blocks to True
        for row in range(3, 15):
            blockGrid[row][1] = True
                
        for row in range(3, 15):
            blockGrid[row][3] = True
                
        for row in range(3, 7):
            blockGrid[row][2] = True
                
        for row in range(11, 15):
            blockGrid[row][2] = True

        return (blockGrid, colorGrid)

    ## LEVEL SIX: takes nothing, returns level's boolean/color grids
    ## # this function makes level six
    def makeLevelSix():

        # initialize variables
        (blockGrid,colorGrid) = makeBlankLevel()
        trueFalse = [True, False]

        # set certain blocks to True, randomly
        for row in range(3, 15):
            for column in range(1, 4):
                blockGrid[row][column] = random.choice(trueFalse)

        return (blockGrid, colorGrid)

    ## LEVEL SEVEN: takes nothing, returns level's boolean/color grids
    ## # this function makes level seven
    def makeLevelSeven():

        # initialize variables
        (blockGrid,colorGrid) = makeBlankLevel()

        # set certain blocks to True
        for row in range(3, 15):
            blockGrid[row][1] = True
            
        for row in range(3, 15):
            blockGrid[row][3] = True

        for row in range(3, 5):
            blockGrid[row][2] = True
                
        for row in range(8, 10):
            blockGrid[row][2] = True
            
        for row in range(13, 15):

            blockGrid[row][2] = True

        return (blockGrid, colorGrid)

    ## LEVEL EIGHT: takes nothing, returns level's boolean/color grids
    ## # this function makes level eight
    def makeLevelEight():
        
        # initialize variables
        (blockGrid,colorGrid) = makeBlankLevel()

        # set certain blocks to True
        for row in range(3, 18):
            blockGrid[row][(row % 3) + 1] = True
            
        blockGrid[16][2] = False
        
        return (blockGrid, colorGrid)

    ## LEVEL NINE: takes nothing, returns level's boolean/color grids
    ## # this function makes level nine
    def makeLevelNine():
        # another random level!
        return makeLevelSix()

    ## LEVEL TEN: takes nothing, returns level's boolean/color grids
    ## # this funtion makes level ten
    def makeLevelTen():

        # initialize variables
        (blockGrid,colorGrid) = makeBlankLevel()

        # set certain blocks to True
        for row in range(3, 20):
            for column in range(1, 4):
                blockGrid[row][column] = True

        for row in range(16, 20):
            blockGrid[row][2] = False

        return (blockGrid, colorGrid)

    # use local functions to make the levels
    (levelOneBlockGrid, levelOneColorGrid) = makeLevelOne()
    (levelTwoBlockGrid, levelTwoColorGrid) = makeLevelTwo()
    (levelThreeBlockGrid, levelThreeColorGrid) = makeLevelThree()
    (levelFourBlockGrid, levelFourColorGrid) = makeLevelFour()
    (levelFiveBlockGrid, levelFiveColorGrid) = makeLevelFive()
    (levelSixBlockGrid, levelSixColorGrid) = makeLevelSix()
    (levelSevenBlockGrid, levelSevenColorGrid) = makeLevelSeven()
    (levelEightBlockGrid, levelEightColorGrid) = makeLevelEight()
    (levelNineBlockGrid, levelNineColorGrid) = makeLevelNine()
    (levelTenBlockGrid, levelTenColorGrid) = makeLevelTen()

    # save correct levels to correct places in the dictionary
    canvas.data["levelOne"] = levelOneBlockGrid
    canvas.data["levelOneColorGrid"] = levelOneColorGrid
    
    canvas.data["levelTwo"] = levelTwoBlockGrid
    canvas.data["levelTwoColorGrid"] = levelTwoColorGrid
    
    canvas.data["levelThree"] = levelThreeBlockGrid
    canvas.data["levelThreeColorGrid"] = levelThreeColorGrid
    
    canvas.data["levelFour"] = levelFourBlockGrid
    canvas.data["levelFourColorGrid"] = levelFourColorGrid
    
    canvas.data["levelFive"] = levelFiveBlockGrid
    canvas.data["levelFiveColorGrid"] = levelFiveColorGrid
    
    canvas.data["levelSix"] = levelSixBlockGrid
    canvas.data["levelSixColorGrid"] = levelSixColorGrid
    
    canvas.data["levelSeven"] = levelSevenBlockGrid
    canvas.data["levelSevenColorGrid"] = levelSevenColorGrid
    
    canvas.data["levelEight"] = levelEightBlockGrid
    canvas.data["levelEightColorGrid"] = levelEightColorGrid
    
    canvas.data["levelNine"] = levelNineBlockGrid
    canvas.data["levelNineColorGrid"] = levelNineColorGrid
    
    canvas.data["levelTen"] = levelTenBlockGrid
    canvas.data["levelTenColorGrid"] = levelTenColorGrid

  ## BLOCKS ##  
  def blockInit():

      ## BLANK LEVEL: takes nothing, returns a blank level
      ## # this function makes a blank level
      def makeBlankLevel():

          # exract information from the dictionary
          rows = canvas.data["rows"]
          columns = canvas.data["columns"]

          # initialize variables
          blockGrid = []

          # set all values to False
          for row in range(rows):
              blockGrid += [[False] * columns]

          return blockGrid
      
      # blocks
      canvas.data["rows"] = 35
      canvas.data["columns"] = 5
      canvas.data["rowStep"] = canvas.data["CANVAS_WIDTH"] // 30
      canvas.data["columnStep"] = canvas.data["CANVAS_WIDTH"] // 5
      canvas.data["blankLevel"] = makeBlankLevel()

      # make lists of the keys for the levels and text displayed on the screen
      # # when the game is paused
      canvas.data["keyLevelList"] = ["levelTen", "levelNine", "levelEight",
                                      "levelSeven", "levelSix", "levelFive",
                                      "levelFour", "levelThree", "levelTwo",
                                      "levelOne"]

      canvas.data["textLevelList"] = ["LEVEL TEN", "LEVEL NINE", "LEVEL EIGHT",
                                      "LEVEL SEVEN", "LEVEL SIX", "LEVEL FIVE",
                                      "LEVEL FOUR", "LEVEL THREE", "LEVEL TWO",
                                      "LEVEL ONE"]

      # make all the levels
      makeLevels()
      levelKey = canvas.data["keyLevelList"].pop()

      # set initial level
      canvas.data["currentBlockGrid"] = canvas.data[levelKey]
      canvas.data["currentColorGrid"] = canvas.data[levelKey+"ColorGrid"]
      canvas.data["currentTextLevel"] = canvas.data["textLevelList"].pop()

  # call all the local functions
  splashInit()
  universalInit()
  gameInit()
  blockInit()

    
## TURN over: takes "canvas", returns None
## # This is called when the ball hits the side.  It is sort of a precursor
## # # to the "reset" This displays a turn over message, waits 1000 ms, and
## # # # and then calls the reset function. Because of the timer, the turnOver
## # # # # function is naturally called twice. Thus, I impliemented a counter
## # # # # # so that it will only diplay one message, instead of one being
## # # # # # # and then quickly replaced with another.
def turnOver(canvas):
  # extract information from the canvas
  textSize = canvas.data["L_TEXT_SIZE"]
  lives = canvas.data["lives"]

  # compute / intitialize variables
  centerX = canvas.data["CANVAS_WIDTH"] // 2
  centerY = canvas.data["CANVAS_HEIGHT"] //2

  # set variables to values needed to stop motion on the screen
  canvas.data["ballVelocityX"] = 0
  canvas.data["ballVelocityY"] = 0
  canvas.data["horizontalPaddleVelocity"] = 0
  canvas.data["verticalPaddleVelocity"] = 0
  canvas.data["delay"] = 2000

  # why "<="? once out of the hundreds (maybe thousands of times) I've
  # # played this, it allowed me to keep going below 0 lives. I don't know
  # # # why. Just in case though, I used <=.
  # # # # If the game is over, set the "lastGamePoints"
  if lives <= 0:
    canvas.data["lastGamePoints"] = canvas.data["points"]

  ## GET a message: takes nothing, returns a message
  ## # local function to return an appropriate turn over message
  def turnOverMessage():
    messages = ["You lost a life!", "Down the drain!", "Try again.",
                "C'mon, you could have got that!", "You suck.",
                "Someone needs practice.", "My grandma can do better.",
                "BOOO!", "WOW! That was great...", "BOMB!",
                "-__-", "o.0", "STRIKE!", "Way to go, nerd."]

    if lives == 0: return "GAME OVER"
    else: return random.choice(messages)
      
  # if statement so it is only drawn once
  if canvas.data["turnOverCounter"] == 1:

      # reset the "turnOverCounter"
      canvas.data["turnOverCounter"] = 0

      # get a message
      message = turnOverMessage()

      # draw the turn over message
      canvas.create_text(centerX, centerY, text = message,
                         font = ("Courier", textSize))
      return # get out of the function, before bad things happen
  
  # if the the game is over, wait a bit, and then return to the
  # # splash screen
  if lives == 0:
      canvas.data["gameOverScreen"] = True
      canvas.after(2000, init, canvas)
      
  # if the game is not over, wait a bit, and reset the game to
  # # keep playing
  elif canvas.data["turnOver"]:
      canvas.after(1000, reset, canvas)

  # incriment the counter
  canvas.data["turnOverCounter"] += 1
        
## RESETS the dictionary: takes "canvas", returns None
## # after a life is lost in gameplay, this functin resets particular
## # # variables so the game can go on
def reset(canvas):
  difficulty = canvas.data["difficulty"]
  # Paddles
  canvas.data["horizontalCenterPaddle"] = canvas.data["CANVAS_WIDTH"] // 2
  canvas.data["verticalCenterPaddle"] = canvas.data ["CANVAS_WIDTH"] // 2
  canvas.data["horizontalPaddleVelocity"] = 0
  canvas.data["verticalPaddleVelocity"] = 0
  canvas.data["paddleColor"] = "black"

  # ball
  canvas.data["ballCenterX"] = canvas.data["CANVAS_WIDTH"] // 2
  canvas.data["ballCenterY"] = canvas.data["CANVAS_HEIGHT"] // 2
  canvas.data["ballVelocityX"] = canvas.data["CANVAS_WIDTH"] // 400
  canvas.data["ballColorCounter"] = 0

  # set the speed of the ball according to the difficulty level
  if difficulty == "hard":
      canvas.data["ballVelocityY"] = canvas.data["CANVAS_WIDTH"] // 55
  elif difficulty == "normal":
       canvas.data["ballVelocityY"] = canvas.data["CANVAS_WIDTH"] // 70
  elif difficulty == "easy":
        canvas.data["ballVelocityY"] = canvas.data["CANVAS_WIDTH"] // 85    

  # general gameplay
  canvas.data["turnOver"] = False
  canvas.data["delay"] = 30
  canvas.data["paused"] = True 

## TIMER: takes "canvas", returns None
## # this is the timer for the game part of the program. It calls the correct
## # # speed functions and redraws everything
def timerFired(canvas):

    # extract information from the canvas
    playGameScreen = canvas.data["playGameScreen"]
    paused = canvas.data["paused"]
    delay = canvas.data["delay"]
    win = canvas.data["winner"]

    # if the game is not paused or the game is not won,
    # # things are permitted to move
    if not paused and not win:

        # move the paddles. usually good for gameplay
        movePaddles(canvas)
       
        # call correct speed function
        if canvas.data["ballVelocityY"] > 0: ballPositiveYVelocity(canvas)
        if canvas.data["ballVelocityX"] > 0: ballPositiveXVelocity(canvas)
        if canvas.data["ballVelocityY"] < 0: ballNegativeYVelocity(canvas)
        if canvas.data["ballVelocityX"] < 0: ballNegativeXVelocity(canvas)

    # redraw, so you can see it.
    redrawAll(canvas)

    # if the game is playing the game (make sense?), call the game timer
    if playGameScreen: 
      canvas.after(delay, timerFired, canvas)

##### END CONTROL CENTER #####
##############################

## RUN the program
## # this function starts the program running
def run():
  # intialize variables
  CANVAS_WIDTH = 700
  CANVAS_HEIGHT = CANVAS_WIDTH
  
  # initialize canvas
  root = Tk()
  canvas = Canvas(root, width=CANVAS_WIDTH, height= CANVAS_HEIGHT, background="white")
  canvas.pack()

  # make it so the window is not resizable
  root.resizable(height = 0, width = 0)

  # give the canvas a title
  root.title("Multegula")

  # Store canvas in root and in canvas itself for callbacks
  root.canvas = canvas.canvas = canvas

  # set up dicitonary
  canvas.data = {}

  # store values in the dictionary that will not need to be reset
  # # when most else needs to be.  These variables will be changed
  # # # in the code as needed
  canvas.data["CANVAS_WIDTH"]  = CANVAS_WIDTH
  canvas.data["CANVAS_HEIGHT"] = CANVAS_HEIGHT
  canvas.data["lastGamePoints"] = 0
  canvas.data["gameOverScreen"] = False
  canvas.data["difficulty"] = None
  canvas.data["winner"] = False

  # sets up events
  root.bind("<Key>", keyPressed)
  root.bind("<Button-1>", mousePressed)

  # let the games begin
  init(canvas)
  redrawAll(canvas)
  
  # This call BLOCKS (so your program waits until you close the window!)
  root.mainloop()
run()
