# EXAMPLE UI CODE FROM BLOCKBUSTER
# For porting to Multegula
# Adapted for Python 3 by Garrett Miller and 2to3 utility
#
# by daniel santoro. ddsantor.

##### IMPORT MODULES #####
from tkinter import *
import random

class Ball:
  def __init__(self, canvas_width, canvas_height):
    self.CANVAS_WIDTH = canvas_width;
    self.CANVAS_HEIGHT = canvas_height;
    self.BORDER_WIDTH = canvas_width // 350;
    self.COLORS = ["red", "green", "blue", "purple", "orange", "yellow"];

    self.color = "green";
    self.xSpeed = 0;
    self.ySpeed = canvas_width // 100;
    self.xCenter = canvas_width // 2;
    self.yCenter = canvas_height // 2;
    self.radius = canvas_width // 50;
    self.borderWidth = canvas_width // 350;

  # change ball color randomly
  def randomBallColor(self):
    currentColor = self.color;
    newColor = currentColor;

    # loop until a new color has been chosen
    while (currentColor == newColor):
      newColor = random.choice(self.COLORS);

    # set new color
    self.color = newColor;

  # randomize X velocity
  def randomXVelocity(self):
    speed = self.CANVAS_WIDTH // 100
    factor = random.random();
    factor *= random.randint(-2, 2);
    self.xSpeed = speed*factor;

  def setXSpeed(self, xSpeed):
    self.xSpeed = xSpeed;

  def setYSpeed(self, ySpeed):
    self.ySpeed = ySpeed;

  def move(self):
    # these variables need to be called here because they are constantly changing
    xCenter = self.xCenter;
    yCenter = self.yCenter;
    xSpeed = self.xSpeed;
    ySpeed = self.ySpeed;
    radius = self.radius;
    CANVAS_WIDTH = self.CANVAS_WIDTH;
    CANVAS_HEIGHT = self.CANVAS_HEIGHT;

    # UPDATE Y VELOCITY - 
    if (((yCenter + radius) >= CANVAS_HEIGHT) and (ySpeed > 0)):
      self.randomXVelocity();
      self.randomBallColor();
      self.ySpeed -= (2*ySpeed);
    elif (((yCenter - radius) <= 0) and (ySpeed < 0)):
      self.randomBallColor();
      self.ySpeed -= (2*ySpeed);
    else: 
      self.yCenter += ySpeed

    # UPDATE X VELOCITY -
    if (((xCenter - radius) <= 0) and (xSpeed < 0)):
      self.randomBallColor();
      self.xSpeed -= (xSpeed*2);
    elif(((xCenter + radius) >= CANVAS_WIDTH) and (xSpeed > 0)):
      self.randomBallColor();
      self.xSpeed -= (xSpeed*2);
    else: 
      self.xCenter += xSpeed; 

  # draw the ball
  def draw(self, canvas):
    color   = self.color;
    borderWidth = self.borderWidth;
    xCenter = self.xCenter;
    yCenter = self.yCenter;
    radius  = self.radius;

    canvas.create_oval(xCenter - radius,
                       yCenter - radius,
                       xCenter + radius,
                       yCenter + radius,
                       fill = color, width = borderWidth)

  def moveAndDraw(self, canvas):
    self.move();
    self.draw(canvas);


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

  ball = Ball(CANVAS_WIDTH, CANVAS_HEIGHT);
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
      ball.moveAndDraw(canvas);
      splashScreenText();
      splashScreenButtons();

      # keep the timer running
      if delay != 0:
        canvas.after(delay, splashTimerFired);

  # get things rolling
  splashTimerFired();

##### END SPLASH SCREEN #####
#############################

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

  # call all the local functions
  splashInit()
  universalInit()
  gameInit()
  #blockInit()

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

  # sets up events
  #root.bind("<Key>", keyPressed)
  #root.bind("<Button-1>", mousePressed)

  # let the games begin
  init(canvas)
  redrawAll(canvas)
  
  # This call BLOCKS (so your program waits until you close the window!)
  root.mainloop()
run()
