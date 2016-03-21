# daniel santoro. ddsantor.

##### IMPORT MODULES #####
from Tkinter import *
import random
import urllib2
##### END IMPORT MODULES ######
###############################

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
    canvasHeight = canvas.data["canvasHeight"]
    canvasWidth = canvas.data["canvasWidth"]
    
    # # button variables
    buttonColor1 = canvas.data["buttonColor1"]
    buttonColor2 = canvas.data["buttonColor2"]
    buttonColor3 = canvas.data["buttonColor3"]
    buttonSize = canvas.data["buttonSize"]
    buttonMargin = canvas.data["buttonMargin"]
    
    # # text variables
    smallTextSize = canvas.data["smallTextSize"]
    mediumSmallTextSize = canvas.data["mediumSmallTextSize"]
    mediumLargeTextSize = canvas.data["mediumLargeTextSize"]
    largeTextSize = canvas.data["largeTextSize"]
    
    # # ball variables  
    splashRadius = canvas.data["splashRadius"]
    ballCenterY = canvas.data["ballCenterY"]

    # # file variable
    fileName = canvas.data["highScoreFileName"]

    # # gameplay variables
    difficulty = canvas.data["difficulty"]

    # COMPUTE/INITIALIZE important variables
    marginX = canvasWidth / 20
    marginY = canvasHeight / 20
    centerX = canvasWidth / 2
    centerY = canvasHeight / 2
    oneQuarterX = canvasWidth / 4
    threeQuartersX = canvasWidth * .75
    
    ## DRAW button: takes the vertical placement of the button, and the lines
    ##              to be written, returns None
    ## # this function draws a button on the canvas. It is called many times
    ## # # by the various 
    def drawButton(verticalMargin, line1, line2):

        # button border
        canvas.create_rectangle(centerX - buttonSize, marginY * verticalMargin,
                                centerX + buttonSize,
                                marginY * (verticalMargin + 2), fill = "black")

        # button's clickable region
        canvas.create_rectangle(centerX - buttonSize + buttonMargin,
                                (marginY * verticalMargin) + buttonMargin,
                                centerX + buttonSize - buttonMargin,
                                (marginY * (verticalMargin + 2)) - buttonMargin,
                                fill = buttonColor1)
        # one line button text
        if line2 == "":
            canvas.create_text(centerX, marginY * (verticalMargin + 1), text = line1,
                               font = ("Helvetica", smallTextSize))
        # two line button text
        else:
            canvas.create_text(centerX, (marginY * (verticalMargin + 1)) - buttonMargin,
                           text = line1,
                           font = ("Helvetica", smallTextSize))
            canvas.create_text(centerX, (marginY * (verticalMargin + 1)) + (2 * buttonMargin),
                           text = line2,
                           font = ("Helvetica", smallTextSize))   
        
    ## DRAW the splash screen background: takes nothing, returns None
    ## # this draws the color part of the background over top of the
    ## # # the black background
    def splashScreenBackGround():
        # This variables are called within the function because they changes as the
        # # user clicks certain places.       
        playGameScreen = canvas.data["playGameScreen"]
        instructionScreen = canvas.data["instructionScreen"]
        gameOverScreen = canvas.data["gameOverScreen"]
        highScoreScreen = canvas.data["highScoreScreen"]
        color = canvas.data["splashScreenColor"]

        # black background
        canvas.create_rectangle(0, 0, canvasWidth, canvasHeight, fill = "black",
                                width = 0)

        # color foreground
        canvas.create_rectangle(marginX, marginY, canvasWidth - marginX,
                                canvasHeight - marginY, fill = color,
                                width = 0)
        
    ## DRAW splash screen text: takes nothing, returns None
    ## # this draws the title and the author over the colored portion of the
    ## # # background.
    def splashScreenText():
        canvas.create_text(centerX, marginY * 3, text = "Welome to...",
                           font = ("Helvetica", mediumLargeTextSize))
        canvas.create_text(centerX, marginY * 5, text = "BLOCK BUSTER",
                           font = ("Helvetica", largeTextSize))
        canvas.create_text(centerX, marginY * 8, text = "created by",
                           font = ("Helvetica", mediumSmallTextSize))
        canvas.create_text(centerX, (marginY * 9), text = "Dan Santoro",
                           font = ("Helvetica", mediumSmallTextSize))

    ## DRAW splash screen buttons: takes nothing, returns None
    ## # this uses local functions to draw each button overtop of the colored
    ## # # part of the background
    def splashScreenButtons():

        ## DRAW first button
        drawButton(10, "Play Game", "")
        
        ## DRAW second button
        drawButton(13, "Instructions", "")

        ## DRAW third button
        drawButton(16, "High Scores", "")

    ## DRAW instruction screen text: takes nothing, returns None
    ## # this function draws the header of the instruction screen along with
    ## # # the rest of the instructions on top of the background and ball
    def instructionScreenText():

        # instruction screen header
        canvas.create_text(centerX, marginY * 3, text = "Instructions",
                           font = ("Helvetica", largeTextSize))

        ## SPLASH SCREEN instructions: takes nothing, returns None
        ## # instructions for how to use the splash screen
        def splashScreenInstructions():

            # sub header
            canvas.create_text(oneQuarterX, marginY * 5,
                               text = "Splash Screen",
                               font = ("Helvetica", mediumLargeTextSize, "underline"))

            # instructions
            canvas.create_text(oneQuarterX, marginY * 6,
                               text = "Use the buttons to navigate.",
                               font = ("Helvetica", smallTextSize))
            canvas.create_text(oneQuarterX, marginY * 7,
                               text = "Do some random clicking to",
                               font = ("Helvetica", smallTextSize))
            canvas.create_text(oneQuarterX, marginY * 8,
                               text = "discover some fun features.",
                               font = ("Helvetica", smallTextSize))             

        ## CONTROL instructions: takes nothing, returns None
        ## # instructions for how to use the paddles to play the game
        def controlInstructions():

            # sub header
            canvas.create_text(threeQuartersX, marginY * 5,
                               text = "Controls",
                               font = ("Helvetica", mediumLargeTextSize, "underline"))

            # instructions
            canvas.create_text(threeQuartersX, marginY * 6,
                               text = "Up, down, left and right",
                               font = ("Helvetica", smallTextSize))
            canvas.create_text(threeQuartersX, marginY * 7,
                               text = " move your paddles, while",
                               font = ("Helvetica", smallTextSize))
            canvas.create_text(threeQuartersX, marginY * 8,
                               text = "the spacebar stops them.",
                               font = ("Helvetica", smallTextSize))
            canvas.create_text(threeQuartersX, marginY * 9,
                               text = "Use 'p' to pause, 'q' to",
                               font = ("Helvetica", smallTextSize))
            canvas.create_text(threeQuartersX, marginY * 10,
                               text = "quit and spacebar or 'p'",
                               font = ("Helvetica", smallTextSize))
            canvas.create_text(threeQuartersX, marginY * 11,
                               text = "to unpause the game.",
                               font = ("Helvetica", smallTextSize))

        ## SCOREING instructions: takes nothing, returns None    
        ## # tells how the game is scored
        def scoringInstructions():

            # sub header
            canvas.create_text(oneQuarterX, marginY * 10,
                               text = "Scoring",
                               font = ("Helvetica", mediumLargeTextSize, "underline"))

            # instructions
            canvas.create_text(oneQuarterX, marginY * 11,
                               text = "Every time the ball hits a",
                               font = ("Helvetica", smallTextSize))
            canvas.create_text(oneQuarterX, marginY * 12,
                               text = "paddle, +points are awarded",
                               font = ("Helvetica", smallTextSize))
            canvas.create_text(oneQuarterX, marginY * 13,
                               text = "A block broken is +5 points.",
                               font = ("Helvetica", smallTextSize))           
            canvas.create_text(oneQuarterX, marginY * 14,
                               text = " Every life lost is -25 points.",
                               font = ("Helvetica", smallTextSize))
            canvas.create_text(oneQuarterX, marginY * 15,
                               text = "Every level passed is +100",
                               font = ("Helvetica", smallTextSize))
            canvas.create_text(oneQuarterX, marginY * 16,
                               text = "points and an extra life.",
                               font = ("Helvetica", smallTextSize))

        ## POWER UP instructions: takes nothing, returns None
        ## # gives the details on power ups
        def powerUpInstructions():

            # sub header
            canvas.create_text(threeQuartersX, marginY * 13,
                               text = "Power-Ups",
                               font = ("Helvetica", mediumLargeTextSize, "underline"))

            # instructions
            canvas.create_text(threeQuartersX, marginY * 14,
                               text = "Red blocks decrease",
                               font = ("Helvetica", smallTextSize))
            canvas.create_text(threeQuartersX, marginY * 15,
                               text = "the size of the paddle.",
                               font = ("Helvetica", smallTextSize))
            canvas.create_text(threeQuartersX, marginY * 16,
                               text = "Green blocks increase",
                               font = ("Helvetica", smallTextSize))
            canvas.create_text(threeQuartersX, marginY * 17,
                               text = "the size of the paddle.",
                               font = ("Helvetica", smallTextSize))
            canvas.create_text(threeQuartersX, marginY * 18,
                               text = "White blocks add a life.",
                               font = ("Helvetica", smallTextSize))
           

        # call all of the instructions
        splashScreenInstructions()
        controlInstructions()
        scoringInstructions()
        powerUpInstructions()
        
    ## DRAW the high score screen text: takes nothing, returns None
    ## # this fuction draws the header of the instrutcion screen along with
    ## # # the rest of the high scores on top of the background and the ball
    def highScoreScreenText():
        
        # draw the header for the screen
        canvas.create_text(centerX, marginY * 3, text = "High Scores",
                           font = ("Helvetica", largeTextSize))
        canvas.create_text(centerX, marginY * 5, text = "Which high scores do you want to see?",
                           font = ("Helvetica", mediumLargeTextSize))

    ## WRITE high scores: takes nothing, returns None
    ## # this function gets the high scores from a file, and then uses a
    ## # # helper function to get the string to be written on the canvas
    ## # # # on the high score screen
    def writeHighScores():

        # This variable is called within the function because it changes as the
        # # user navigates through certain menus.  If it was called with the rest
        # # # of the variables the high scores would stay the same
        difficulty = canvas.data["difficulty"]

        # extract information from the dictionary / initialize variables
        count = 6 # this doubles as the position of the score and the place on the list
        highScoreList = canvas.data["highScoreList"]

        # DETERMINE the header for the high score screen
        # # pro scores header
        if difficulty == "hard":
            canvas.create_text(centerX, marginY * 3, text = "Pro Scores",
                               font = ("Helvetica", largeTextSize))
        # # joe scores header
        elif difficulty == "normal":
            canvas.create_text(centerX, marginY * 3, text = "Joe Scores",
                               font = ("Helvetica", largeTextSize))

        # # hobo scores header
        elif difficulty == "easy":
            canvas.create_text(centerX, marginY * 3, text = "Hobo Scores",
                               font = ("Helvetica", largeTextSize))

        # # this will never happen
        else:
            canvas.create_text(centerX, marginY * 3, text = "High Scores",
                               font = ("Helvetica", largeTextSize))
            

        # This uses a for loop to draw all of the high scores if the file exists
        if highScoreList != "High Scores Not Found":

            # subheader
            canvas.create_text(centerX / 5, marginY * 5,
                               text = "Place ---- Date ---- Name ---- Score",
                               font = ("Courier", mediumSmallTextSize, "bold"),
                               anchor = "sw")


            # use a for loop to draw the all of the scores on the screen           
            for score in highScoreList:

                # use a helper function to get the format of the string to be
                # # drawn on the screen
                message = scoreDisplayString(score,  count - 5)

                canvas.create_text(centerX / 5, marginY * count, text = message,
                                   font = ("Courier", mediumSmallTextSize),
                                   anchor = "sw")
                count += 1

        # this happens if the high score file does not exist
        else:
            canvas.create_text(centerX, centerY,
                               text = "High Scores Not Found",
                               font = ("Courier", mediumLargeTextSize, "bold"))            
            
    # DRAW buttons for the: takes nothing, returns None 
    def highScoreScreenButtons():
        ## DRAW first button
        drawButton(7, "Pro Scores", "")

        ## DRAW second button
        drawButton(10, "Joe Scores", "")
            
        ## DRAW third button
        drawButton(13, "Hobo Scores", "")

    
    ## GET string to be written on the canvas: takes nothing, returns None
    ## # This function is passed a score tuple and the place on the high
    ## # # score list. It returns a string formatted to be written on the
    ## # # # high score screen.
    def scoreDisplayString(scoreTuple, place):
        
        # initialize variables
        dateBound = ","
        nameBound1 = ", "
        nameBound2 = " -"
        scoreString = "#"
        maxScore = 0

        # compute variables
        dateIndex = scoreTuple[0].find(dateBound)
        nameIndex1 = scoreTuple[0].find(nameBound1) + len(nameBound1)
        nameIndex2 = scoreTuple[0].find(nameBound2)
        date = scoreTuple[0][:dateIndex]
        name = scoreTuple[0][nameIndex1:nameIndex2]


        # edit the date if it's not found
        if date == "No Date Found":
            date = "None"
            
        # add the numerical place on the high score list to the string
        scoreString += str(place)

        # Add spaces to the string until it's length is 10 (for formatting)
        while len(scoreString) <= 10:
            scoreString += " "

        # add the date to the string 
        scoreString += date

        # add spaces to the string until it's length is 20 (for formatting)
        while len(scoreString) <= 20:
            scoreString += " "

        # add the name to the string
        scoreString += name

        # add spaces to the string until it's length is 30 (for formatting)
        while len(scoreString) <= 30:
            scoreString += " "

        # add the score to the string
        scoreString += str(scoreTuple[1])
    
        return scoreString
                                
    ## DRAW the play screen text: takes nothing, returns None
    ## # this function draws the header and 'instruction' for the play screen
    ## # # over top of the background and the ball
    def playGameScreenText():

        # header
        canvas.create_text(centerX, marginY * 3, text = "Bust Some Blocks",
                           font = ("Helvetica", largeTextSize))

        # sub header
        canvas.create_text(centerX, marginY * 5, text = "Click the one that applies.",
                           font = ("Helvetica", mediumLargeTextSize))

    ## DRAW the buttons on the play screen: takes nothing, returns None
    ## # this fucntion draws the first three buttons on the play screen
    ## # # starting with hard, and ending with easy
    def playGameScreenButtons():

        ## DRAW first button -- hard
        drawButton(7, "I'm a Pro", "")

        ## DRAW second button -- normal
        drawButton(10, "I'm a Joe.", "")
            
        ## DRAW third button -- easy
        drawButton(13, "I'm a hobo.", "")

    ## DRAW game over screen: takes nothing, returns None
    ## # This function draws the screen that will show up right after the game
    ## # # is over. It displays a header and gives the player and opportunity
    ## # # # to input their name to be added to the high score list.
    def gameOverScreen():

        # extract information from the dicitonary
        name = canvas.data["name"]

        # incriment counter
        canvas.data["delayCounter"] += 1

        # header
        canvas.create_text(centerX, marginY * 3, text = "GAME OVER",
                           font = ("Helvetica", largeTextSize))

        # instructions
        canvas.create_text(centerX, marginY * 6, text = "Type your name below to claim",
                           font = ("Helvetica", mediumLargeTextSize))
        canvas.create_text(centerX, marginY * 7, text = "your spot among the elite.",
                           font = ("Helvetica", mediumLargeTextSize))         

        # sub header
        canvas.create_text(oneQuarterX, marginY * 11, text = "Your name:",
                           font = ("Helvetica", mediumSmallTextSize),
                           anchor = "sw")

        # this makes the cursor at the end of the name blink
        if canvas.data["delayCounter"] % 36 < 18:
            canvas.create_text(centerX - (oneQuarterX / 5), marginY * 11,
                               text = name + "|",
                               font = ("Helvetica", mediumSmallTextSize),
                               anchor = "sw")
        else:
            canvas.create_text(centerX - (oneQuarterX / 5), marginY * 11,
                               text = name,
                               font = ("Helvetica", mediumSmallTextSize),
                               anchor = "sw")
            
    ## DRAW game over buttons: takes nothing, returns None
    ## # This function draws the button that will show up on the game over
    ## # # screen.
    def gameOverScreenButtons():

        drawButton(13, "High Scores", "")
        
    # this funtion does not use the "drawButton" helper function: takes nothing, returns None
    def returnToHighScoreScreenButton():

        drawButton(16, "Return to", "score screen")
            
    ## DRAW the return to main screen button: takes nothing, returns None
    ## # this function draws the button that appears on all branches of
    ## # the splash sceeen.  
    def returnToMainScreenButton():

        drawButton(16, "Return to", "main screen")

    ## DRAW and MOVE the ball: takes nothing, returns None
    ## # This function does almost everything that pertains to the bouncing
    ## # # ball. From determining it's color, to drawing it, to making it move
    ## # # # this is all accomplished with local functions.
    def ball():

        ## BALL color
        ## # determines the color of the ball, randomly
        def splashColorOfBall():

            # extract information from the dictionary
            currentColor = canvas.data["splashColorOfBall"]
            
            # BALL color options
            colors = ["red", "white", "green", "blue", "purple", "orange",
                      "yellow"]

            # loop until the conditions are met
            while True:
                color = random.choice(colors)

                if color != canvas.data["splashScreenColor"] and color != currentColor:
                    return color
                
        ## DRAW ball: takes nothing, returns None
        ## # draws the ball...suprise!
        def drawBall():

            # the reason this variables are called here and not with the rest
            # # of the variables at the top of the funtion is because if they
            # # # were called there and not here the ball would not move becuase
            # # # # these variables are constantly changing
            color = canvas.data["splashColorOfBall"]
            borderWidth = canvas.data["borderWidth"]
            ballCenterX = canvas.data["ballCenterX"]
            ballCenterY = canvas.data["ballCenterY"]

            # so the ball isn't all white
            if color == "white":
                otherColor = "black"
            else:
                otherColor = "white"

            canvas.create_oval(ballCenterX - splashRadius,
                               ballCenterY - splashRadius,
                               ballCenterX + splashRadius,
                               ballCenterY + splashRadius,
                               fill = color, width = borderWidth)
            canvas.create_oval(ballCenterX - splashRadius + (splashRadius / 3.5),
                               ballCenterY - splashRadius + (splashRadius / 3.5),
                               ballCenterX + splashRadius - (splashRadius / 3.5),
                               ballCenterY + splashRadius - (splashRadius / 3.5),
                               fill = otherColor, width = borderWidth)
            canvas.create_oval(ballCenterX - splashRadius + (splashRadius / 1.5),
                               ballCenterY - splashRadius + (splashRadius / 1.5),
                               ballCenterX + splashRadius - (splashRadius / 1.5),
                               ballCenterY + splashRadius - (splashRadius / 1.5),
                               fill = "red", width = borderWidth)

        ## BALL moving right: takes nothing, returns None
        ## # handles the x movement of the ball while the ball is moving right
        def ballPositiveXVelocity():

            # these variables need to be called here because they are constantly changing
            ballCenterX = canvas.data["ballCenterX"]
            splashBallVX = canvas.data["splashBallVX"]
            
            # BALL left of the right edge
            if ballCenterX < (canvasWidth - splashRadius):
                canvas.data["ballCenterX"] += splashBallVX
                
            # BALL at left edge
            if ballCenterX >= (canvasWidth - splashRadius):
                canvas.data["splashBallVX"] -= (splashBallVX*2)
                
        ## BALL moving left: takes nothing, returns None
        ## # handles the x movement of the ball while the ball is moving left
        def ballNegativeXVelocity():
            
            # these variables need to be called here because they are constantly changing
            ballCenterX = canvas.data["ballCenterX"]
            splashBallVX = canvas.data["splashBallVX"]
            
            # BALL to the right of the left edge
            if ballCenterX > (splashRadius):
                canvas.data["ballCenterX"] += splashBallVX

            # BALL at the left edge of the screen
            if ballCenterX <= (splashRadius):
                canvas.data["splashBallVX"] = abs(splashBallVX)

        ## BALL moving down: takes nothing, returns None
        ## # handles the y movement of the ball while moving down
        def ballPositiveYVelocity():

            # these variables need to be called here because they are constantly changing
            ballCenterY = canvas.data["ballCenterY"]
            splashBallVY = canvas.data["splashBallVY"]

            # BALL above the bottom of the screen
            if ballCenterY < (canvasHeight - splashRadius):

                canvas.data["ballCenterY"] += splashBallVY

            # BALL at/below the bottom of the screen
            if ballCenterY >= (canvasHeight - splashRadius):
                    determineXVelocityOfBall()
                    canvas.data["splashBallVY"] = -splashBallVY
                    canvas.data["splashColorOfBall"] = splashColorOfBall()
                
        ## BALL moving up: takes nothing, returns None
        ## # handles the y movement of the ball while moving up
        def ballNegativeYVelocity():
            
            # these variables need to be called here because they are constantly changing
            ballCenterY = canvas.data["ballCenterY"]
            splashBallVY = canvas.data["splashBallVY"]
            
            # BALL below the top of the screen
            if ballCenterY > (splashRadius):                       
                canvas.data["ballCenterY"] += splashBallVY

            # BALL at the top of the screen
            if ballCenterY <= (splashRadius):
                canvas.data["splashBallVY"] = abs(splashBallVY)

        ## BALL x velocity determinate: takes nothing, returns None
        ## # determines the x velocity, randomly
        def determineXVelocityOfBall():

            velocityFactor = random.random()
            velocityFactor *= random.randint(-2, 2)

            canvas.data["splashBallVX"] = (canvas.data["splashBallVY"] * velocityFactor)

        ## CALL apppropriate velocity function: takes nothing, returns None
        ## # determines with velocity function to call to move the ball in
        ## # # the correct direction
        def callAppropriateVelocityFunction():
    
            if canvas.data["splashBallVY"] > 0:
                ballPositiveYVelocity()
            if canvas.data["splashBallVX"] > 0:
                ballPositiveXVelocity()
            if canvas.data["splashBallVY"] < 0:
                ballNegativeYVelocity()
            if canvas.data["splashBallVX"] < 0:
                ballNegativeXVelocity()

        # call functions to get the ball moving
        callAppropriateVelocityFunction()
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
            splashScreenBackGround()
            ball()

            # instruction screen?
            if canvas.data["instructionScreen"]:
                instructionScreenText()
                returnToMainScreenButton()

            # high score screen?
            elif canvas.data["highScoreScreen"]:

                # write the high scores?
                if canvas.data["writeHighScores"]:
                    writeHighScores()
                    returnToHighScoreScreenButton()

                # high scores not written yet
                else:
                    highScoreScreenText()
                    highScoreScreenButtons()
                    returnToMainScreenButton()

            # play game screen ?
            elif canvas.data["playGameScreen"]:
                playGameScreenText()
                playGameScreenButtons()
                returnToMainScreenButton()

            # game over screen ? (only if the score is good enough to
            # # be placed on the high score list)
            elif canvas.data["gameOverScreen"] and \
                 (canvas.data["lastGamePoints"] > \
                  getHighScores(canvas, difficulty + fileName)[-1][1]):
                gameOverScreen()
                gameOverScreenButtons()
                returnToMainScreenButton()

            # begining screen
            else:
                canvas.data["gameOverScreen"] = False
                splashScreenText()
                splashScreenButtons()

            # keep the timer running
            if delay != 0:
                canvas.after(delay, splashTimerFired)

    # get things rolling
    splashTimerFired()

## SPLASH COLOR: takes "canvas", returns a color
## # this function for the splash screen had to be outside of the splash screen
## # # fuction because it is called by the keypressed function, not by the splash
## # # # screen function itself.
def splashScreenColor(canvas):
    currentColor = canvas.data["splashScreenColor"]
    colors = ["red", "white", "green", "blue", "purple", "orange", "yellow"]
    while True:
        color = random.choice(colors)
        if color != canvas.data["splashColorOfBall"] and color != currentColor:
            return color



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
    fontSize = canvas.data["smallTextSize"]
    level = canvas.data["currentTextLevel"]
    
    # # canvas
    canvasWidth = canvas.data["canvasWidth"]
    canvasHeight  = canvas.data["canvasHeight"]
    outsideMargin = canvas.data["outsideMargin"]

    # # gameplay
    difficulty = canvas.data["difficulty"]


    # compute / initialize variables
    # # text
    sideString = ""
    
    # # canvas
    outsideMargin = outsideMargin * .75
    oneQuarterX = canvasWidth / 4
    threeQuartersX = canvasWidth * .75
    centerX = canvasWidth / 2
    centerY = canvasHeight / 2
    centerTopMargin = (outsideMargin / 1.5)
    centerBottomMargin = canvasHeight - (outsideMargin / 3)
    centerLeftMargin = outsideMargin / 2
    centerRightMargin = canvasWidth - (outsideMargin / 3)

    # draw background
    canvas.create_rectangle(0, 0, canvasWidth, canvasHeight, fill = "black")
    
    canvas.create_rectangle(outsideMargin, outsideMargin,
                           canvasWidth - outsideMargin,
                           canvasHeight - outsideMargin,
                           fill = "white")

    canvas.create_rectangle(0, 0, outsideMargin, outsideMargin,
                            fill = "white")

    # draw header
    canvas.create_text(oneQuarterX, centerTopMargin,
                       text = "Lives: " + str(canvas.data["lives"]),
                       font = ("Helvetica", fontSize), fill = "white")
    canvas.create_text(centerX, centerTopMargin,
                       text = "Points: " + str(canvas.data["points"]),
                       font = ("Helvetica", fontSize), fill = "white")
    canvas.create_text(threeQuartersX, centerTopMargin,
                       text = level,
                       font = ("Helvetica", fontSize), fill = "white")

    # draw footer
    if difficulty == "hard": message = "Pro"
    elif difficulty == "normal": message = "Joe"
    elif difficulty == "easy": message = "Hobo"

    # # display different footer messages if the ai is enabled or if not
    if canvas.data["ai"]:
        canvas.create_text(centerX, centerBottomMargin,
                           text = "You are in A.I. mode! Press 'q' to quit or the spacebar to resume.",
                           font = ("Helvetica", fontSize), fill = "white")

    else:
        canvas.create_text(centerX, centerBottomMargin,
                           text = "You're a " + message + ".",
                           font = ("Helvetica", fontSize), fill = "white")

    # draw sides
    # # create a string to put on the sides
    # # # NOT hobo
    if message != "Hobo":
        for newLine in xrange(10):
            sideString += "\n"
        for char in message:

            sideString += char
            
            for newLine in xrange(10):
                sideString += "\n"
    # # # hobo
    else:
        for newLine in xrange(7):
            sideString += "\n"
        for char in message:
            sideString += char

            for newLine in xrange(7):
                sideString += "\n"

    # # draw the strings on the sides
    canvas.create_text(centerLeftMargin, centerY, text = sideString,
                       font = ("Helvetica", fontSize), fill = "white")                       
    canvas.create_text(centerRightMargin, centerY, text = sideString,
                       font = ("Helvetica", fontSize), fill = "white")            
        

    
                      
## DRAW paused screen: takes "canvas", returns None
## # this function draws a paused screen that occurs often throughout the
## # # the play of the game.
def drawPausedScreen(canvas):

    # extract information from the canvas
    # # text
    message = canvas.data["currentTextLevel"]
    largeFont = canvas.data["largeTextSize"]
    smallFont = canvas.data["mediumLargeTextSize"]
    
    # # canvas
    canvasWidth = canvas.data["canvasWidth"]
    canvasHeight  = canvas.data["canvasHeight"]

    # # gameplay
    lives = canvas.data["lives"]

    # compute / initialize variables
    canvas.data["pausedCounter"] += 1
    centerY = canvasHeight / 2
    centerX = canvas.data["canvasWidth"] / 2
    marginY = canvas.data["canvasHeight"] / 20

    # print the level
    canvas.create_text(centerX, centerY, text = message,
                       font = ("Helvetica", largeFont))

    # alternate the lines printed vial the delay counter
    # # print first line
    if canvas.data["pausedCounter"] % 70 < 35:

        # whether or not to use "start" or "resume"
        if lives == 3 and message == "LEVEL ONE":
            canvas.create_text(centerX, marginY * 12,
                               text = "Press the spacebar to start,",
                               font = ("Helvetica", smallFont))
        else:
            canvas.create_text(centerX, marginY * 12,
                               text = "Press spacebar to resume,",
                               font = ("Helvetica", smallFont))

    # # print second line
    elif canvas.data["pausedCounter"] % 70 > 35:
        canvas.create_text(centerX, marginY * 13,
                           text = "or 'q' to quit the current game.",
                           font = ("Helvetica", smallFont))


    
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
    canvasHeight = canvas.data["canvasHeight"]

    # draw paddle at the bottom of the screen
    canvas.create_rectangle(horizontalCenterPaddle - paddleWidth,
                            canvasHeight - paddleHeight - outsideMargin,
                            horizontalCenterPaddle + paddleWidth,
                            canvasHeight - outsideMargin,
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
    canvasWidth = canvas.data["canvasWidth"]


    # draw paddle on the left
    canvas.create_rectangle(outsideMargin,
                            verticalCenterPaddle - paddleWidth,
                            outsideMargin + paddleHeight,
                            verticalCenterPaddle + paddleWidth,
                            fill = color, width = borderWidth)

    # draw paddle on the right
    canvas.create_rectangle(canvasWidth - outsideMargin - paddleHeight,
                            verticalCenterPaddle - paddleWidth,
                            canvasWidth - outsideMargin,
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
    canvasHeight = canvas.data["canvasHeight"]
    canvasWidth = canvas.data["canvasWidth"]
    outsideMargin = canvas.data["outsideMargin"]

    # moves the horizontal pads (the top and the bottom ones)
    def moveHorizontalPaddles():

        # if the pad isn't all the way to the left or right, let it move
        if (horizontalCenterPaddle + paddleWidth + outsideMargin + (paddleHeight / 2) <= canvasWidth) and \
           (horizontalCenterPaddle - paddleWidth - outsideMargin - (paddleHeight / 2) >= 0):
           
            canvas.data["horizontalCenterPaddle"] += canvas.data["horizontalPaddleVelocity"]    

        # don't let the pad move if it's all the way to the right 
        elif horizontalCenterPaddle + paddleWidth + outsideMargin + (paddleHeight / 2) > canvasWidth:
            canvas.data["horizontalCenterPaddle"] = canvasWidth - paddleWidth - outsideMargin - paddleHeight
            canvas.data["horizontalPaddleVelocity"] = 0

        # don't let the pad move if it's all the way to the left
        elif horizontalCenterPaddle - paddleWidth - outsideMargin - (paddleHeight / 2) < 0:
            canvas.data["horizontalCenterPaddle"] = paddleWidth + outsideMargin + paddleHeight
            canvas.data["horizontalPaddleVelocity"] = 0

    # moves the vertical pads (left and right ones)
    def moveVerticalPaddles():

        # if the pad isn't all the way to the top or the bottom, let it move
        if (verticalCenterPaddle - paddleWidth - outsideMargin - (paddleHeight / 2) >= 0) and \
           (verticalCenterPaddle + paddleWidth + outsideMargin + (paddleHeight / 2) <= canvasHeight):

            canvas.data["verticalCenterPaddle"] += canvas.data["verticalPaddleVelocity"]

        # if the pad is at the top, don't let it move
        elif verticalCenterPaddle - paddleWidth - outsideMargin - (paddleHeight / 2) < 0:
            canvas.data["verticalCenterPaddle"] = paddleWidth + outsideMargin + paddleHeight
            canvas.data["verticalPaddleVelocity"] = 0

        # if the pad is at the bottom, don't let it move
        elif verticalCenterPaddle + paddleWidth + outsideMargin + (paddleHeight / 2) > canvasHeight:
            canvas.data["verticalCenterPaddle"] = canvasHeight - paddleWidth - outsideMargin - paddleHeight
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
    minPaddleWidth = canvas.data["canvasWidth"] / 7

    # # canvas
    canvasHeight = canvas.data["canvasHeight"]

    # # gameplay
    pointsPerHit = canvas.data["pointsPerHit"]

    
    # ball above the bottom pad
    if ballCenterY < (canvasHeight - radius - paddleHeight - outsideMargin):

        canvas.data["ballCenterY"] += ballVelocityY

    # ball at/below the bottom pad
    elif ballCenterY >= (canvasHeight - radius - paddleHeight - outsideMargin):
        # pad below the ball?
        if (horizontalCenterPaddle - paddleWidth) <= ballCenterX <= (horizontalCenterPaddle + paddleWidth): 
            canvas.data["ballVelocityY"] -= (ballVelocityY * 2)
            canvas.data["points"] += pointsPerHit
            canvas.data["ballColorCounter"] += 1

            # determine the x direction of the ball (based on where it hits)
            ballXDirectionDeterminate(canvas)
            
        # pad not below the ball
        elif ballCenterY >= (canvasHeight - outsideMargin):
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
    minPaddleWidth = canvas.data["canvasWidth"] / 7
    
    # # canvas
    canvasHeight = canvas.data["canvasHeight"]

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
    minPaddleWidth = canvas.data["canvasWidth"] / 7
    # # canvas
    canvasWidth = canvas.data["canvasWidth"]    

    # gameplay
    pointsPerHit = canvas.data["pointsPerHit"]

    # ball to the left of the right pad
    if ballCenterX < (canvasWidth - radius - paddleHeight - outsideMargin):
        canvas.data["ballCenterX"] += ballVelocityX

    # ball at/to the right of the right pad
    if ballCenterX >= (canvasWidth - radius - paddleHeight - outsideMargin):

        # pad to the right of the ball?
        if (verticalCenterPaddle - paddleWidth) < ballCenterY < (verticalCenterPaddle + paddleWidth):
            canvas.data["ballVelocityX"] -= (ballVelocityX*2)
            canvas.data["points"] += pointsPerHit
            canvas.data["ballColorCounter"] += 1

        # pad not to the right of the ball
        elif ballCenterX >= canvasWidth - outsideMargin:
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
    minPaddleWidth = canvas.data["canvasWidth"] / 7
    
    # # canvas
    canvasWidth = canvas.data["canvasWidth"]    

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
    paddleFactor = canvas.data["paddleWidth"] / 6.0
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
        velocityFactor = (horizontalCenterPaddle - ballCenterX) / 100.0

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
        velocityFactor = (ballCenterX - horizontalCenterPaddle) / 100.0

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
    for column in xrange(blockColumns):
        for row in xrange(blockRows):
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
    canvasWidth = canvas.data["canvasWidth"]

    # # paddle
    paddleWidth = canvas.data["paddleWidth"]

    # # grid
    rowStep = canvas.data["rowStep"]
    columnStep = canvas.data["columnStep"]
    blockGrid = canvas.data["currentBlockGrid"]
    colorGrid = canvas.data["currentColorGrid"]
    blankLevel = canvas.data["blankLevel"]
    
    # # canvas
    canvasWidth = canvas.data["canvasWidth"]
    # # paddle
    paddlWidth = canvas.data["paddleWidth"]

    # compute variabels
    maxPaddleWidth = canvasWidth / 4
    minPaddleWidth = canvasWidth / 7


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
        row = int(((ballCenterY) - radius) / rowStep)
        column = int(ballCenterX / columnStep)

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
        row = int(((ballCenterY) + radius) / rowStep)
        column = int(ballCenterX / columnStep)

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
        row = int(ballCenterY / rowStep)
        column = int(((ballCenterX) - radius) / columnStep)

        # test for a block, and readjust vaiables
        if blockGrid[row][column]:
            
            # reverse direction
            canvas.data["ballVelocityX"] *= -1

            # check powerups/ break blocks
            breakBlockPowerUp(row, column)

            return # return out before bad things happen

        # reset the column. this will only trip used in very specific cases when
        # # when half or less of the ball is in a given column
        column = int(((ballCenterX) + radius) / columnStep)

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
        row = (ballCenterY / rowStep)
        column = int(((ballCenterX) + radius) / columnStep)

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
The next block of code deals entirly with the high scores.
Web scraping is used to get the date, and there are three .txt files
that hold the high scores for the different levels of the game. I chose to
do three separate files so that each level would be independend of the other,
and Python would only have to go through 10 high scores instead of 30 everytime
a game is over or the user wants to look at a certain set of highscores.
"""
#######################
##### HIGH SCORES #####

## GET time: takes a url, returns the date
## # this function uses web scaping to get the time.  This is used
## # # to identify the highScore
def getDate(url):

    # try to scrape the webpage. If it doesn't work, say "No Date Found"
    try:

        # initialize varialbes
        leftBound = "<BR>"
        rightBound = ", "

        # open the webpage, put all the lines in a list, and close the webpage
        webPage = urllib2.urlopen(url)
        webLines = webPage.readlines()
        webPage.close()

        # use a for loop to to look for the Eastern Time (which is CMU time, which is God's time)
        # # 
        for line in webLines:
            if "Eastern Time" in line:
                index1 = line.find(leftBound)
                index2 = line.find(rightBound)
                return line[index1 + len(leftBound) : index2]
    except:

        # only happens when the internet is not available
        return "No Date Found"

## GET high scores: takes "canvas" and a fileName, returns None
## # This function retrieves the high scores from file, if it exists, and
## # # saves them to the dictionary as a list of tuples
def getHighScores(canvas, fileName):
    # initialize variables
    bound = "- "
    count= 0
    highScoreList = []

    # try and open the file
    try:

        # open file, put the lines in a list, close the file
        highScoreFile = open(fileName)

        # read the file
        highScoreList = highScoreFile.readlines()

        # close the file
        highScoreFile.close()

        
        # loop over the score as a string to cut it down to what is needed
        # # for the program
        for score in highScoreList:

            # find indices to split the string
            index = score.find(bound) + len(bound)

            if "\n" in score:
                endBound = score.find("\n")
            else:
                endBound = len(score)
                
            # set the score up as tuple
            score = (score[:index].strip(), int(score[index:endBound]))

            # this resets each element in the high score list to the
            # # the tuple that was just created
            highScoreList[count] = score
            count += 1
        
        canvas.data["highScoreList"] = highScoreList

    # only happens if the files do not exist
    except:
        canvas.data["highScoreList"] = "High Scores Not Found"

    return canvas.data["highScoreList"]

## RESET: takes canvas, returns None
## # reset the high scores
def resetHighScores(canvas):

    # extract information from the dictionary
    date = canvas.data["date"]
    name = canvas.data["name"]
    currentScore = canvas.data["lastGamePoints"]
    difficulty = canvas.data["difficulty"]
    fileName = canvas.data["highScoreFileName"]

    # initialize variable
    highScoreList = getHighScores(canvas, difficulty + fileName)

    # reset appropriate variable
    if name == "Type name please." or name == "":
        name = "Unknown"

    for count in xrange(9):       
        if (" " * count) == name:

            name = "Unknown"
        
    # make sure there is a highScoreList
    if highScoreList != "High Scores Not Found":

        # checks if the last score is better than the last one in the list
        if currentScore >= (highScoreList[-1][1]):
            
            highScoreList.pop()
            highScoreList.append((date + ", " + \
                                  name + " -", currentScore))
            
        # sort the list  with a helper function
        canvas.data["highScoreList"] = sortHighScoreList(highScoreList)

        # save the high scores
        saveHighScores(canvas)


## SAVE: takes "canvas", returns None
## # save the high scores
def saveHighScores(canvas):

    # extract information from the dictionary
    fileName = canvas.data["highScoreFileName"]
    highScoreList = canvas.data["highScoreList"]
    difficulty = canvas.data["difficulty"]

    # initialize variables
    highScoreString = ""

    # loop through the list of high score tuples, and format them
    # # such that they each date, name and score is in a string
    # # # and only one score per line
    for index in xrange(len(highScoreList)):
        highScoreString += highScoreList[index][0] + " " + \
                           str(highScoreList[index][1]) + "\n"

    # open file for writing, write to the file, close the file
    highScoreFile = open(difficulty + fileName, "wt")

    # write to file
    highScoreFile.write(highScoreString)

    # close the file
    highScoreFile.close()
    
    
## SORT: takes a high score list, and returns that list sorted
## # sort the highScores
def sortHighScoreList(highScoreList):

    # initialize variables
    justScores = []
    newHighScoreList = []

    # make a list of just the scores
    for score in highScoreList:
        justScores.append(score[1])

    # sort the scores from highest to lowest
    justScores.sort()
    justScores.reverse()

    # least efficent part of the program!
    # # use a nested loop to compare the sorted scores to the
    # # # unsorted scores
    # # # # NOTE: a nested loop is okay here because at most it
    # # # # # will only loop 100 times
    for sortedScore in justScores:
        for unsortedScore in highScoreList:
            if sortedScore == unsortedScore[1]:
                newHighScoreList.append(unsortedScore)
                highScoreList.remove(unsortedScore)

    # return the unefficient work 
    return newHighScoreList
        
##### END HIGH SCORES #####
###########################

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

## AI: takes "canvas", returns None
## # this function controls all of the A.I. for the game.
## # # WATCH OUT! COMPUTERS ARE TAKING OVER THE WORLD! Well, at least the game.
def ai(canvas):

    # extract information from the canvas
    # # screens
    playGameScreen = canvas.data["playGameScreen"]
    instructionScreen = canvas.data["instructionScreen"]
    gameOverScreen = canvas.data["gameOverScreen"]
    highScoreScreen = canvas.data["highScoreScreen"]

    # # gameplay
    paused = canvas.data["paused"]
    lives = canvas.data["lives"]

    # incriment counter
    canvas.data["aiCounter"] += 1

    if lives == 0:
        canvas.data["points"] = 1000000

    # unpause if necessary
    if canvas.data["aiCounter"] % 200 == 100 and paused:

        canvas.data["paused"] = False

    # type a message after the A.I. wins
    elif canvas.data["aiCounter"] % 20 == 10 and gameOverScreen:

        # erase the message that's already in the dictionary
        if canvas.data["name"] == "Type name please.": canvas.data["name"] = ""

        # print name
        elif len(canvas.data["aiName"]) > 0: canvas.data["name"] += canvas.data["aiName"].pop()

        # erase name
        elif canvas.data["name"] == "A.I.": canvas.canvas.data["name"] = ""

        # print message
        elif len(canvas.data["aiMessage"]) > 0: canvas.data["name"] += canvas.data["aiMessage"].pop()

        # end the AI
        elif len(canvas.data["aiMessage"]) == 0:
            canvas.data["name"] = ""
            canvas.data["ai"] = False
            canvas.data["gameOverScreen"] = False

    # move the paddles
    aiMovePaddles(canvas)

    # if the "ai" is set, keep calling the ai function
    if canvas.data["ai"]: canvas.after(30, ai, canvas)

## MOVE the ai paddles: takes "canvas", returns None
## # this function moves the paddles with the AI
def aiMovePaddles(canvas):

    # extract information from the canvas
    # # ball
    ballCenterX = canvas.data["ballCenterX"]
    ballCenterY = canvas.data["ballCenterY"]
    ballVelocityX = canvas.data["ballVelocityX"]
    ballVelocityY = canvas.data["ballVelocityY"]

    # # paddle
    verticalPaddleCenter = canvas.data["verticalCenterPaddle"]
    horizontalPaddleCenter = canvas.data["horizontalCenterPaddle"]
    paddleWidth = canvas.data["paddleWidth"]

    # # gameplay
    ballTarget = canvas.data["ballTarget"]
    paused = canvas.data["paused"]
    gameOverScreen = canvas.data["gameOverScreen"]
    winner = canvas.data["winner"]

    # # canvas
    canvasWidth = canvas.data["canvasWidth"]

    # # compute variables
    marginOfError = canvasWidth / 23
    paddleVelocity = canvasWidth / 70

    # if the game is not paused, not over, and there is no winner, move the paddles
    if not paused and not gameOverScreen and not winner:
        
        # moves the vertical paddles
        if verticalPaddleCenter != ballCenterY:

            # allows for a margin of error. in this case the range is based on the
            # # center of the paddle
            if -marginOfError < verticalPaddleCenter - ballCenterY < marginOfError:
                pass # if the ball is within the range, do nothing!

            # move the paddle if the ball is not in the range
            elif verticalPaddleCenter > ballCenterY:
                canvas.data["verticalCenterPaddle"] -= paddleVelocity

            # move the paddle if the ball is not in the range
            elif verticalPaddleCenter < ballCenterY:
                canvas.data["verticalCenterPaddle"] += paddleVelocity

        # move the horizontal paddles

        # # ball moving up
        if ballVelocityY < 0:

            if horizontalPaddleCenter != ballCenterX:

                # allows for a margin of error. in this case the range is based on
                # # the center of the paddle
                if -marginOfError < horizontalPaddleCenter - ballCenterX < marginOfError:
                    pass # if the ball is within the range, do nothing!

                # move the paddle if the ball is not in the range
                elif horizontalPaddleCenter > ballCenterX:
                    canvas.data["horizontalCenterPaddle"] -= paddleVelocity

                # move the paddle if the ball is not in the range
                elif horizontalPaddleCenter < ballCenterX:
                    canvas.data["horizontalCenterPaddle"] += paddleVelocity


            # so when the ball is moving down, it will get a random target
            canvas.data["needTarget"] = True

        # # ball moving down
        elif ballVelocityY > 0:

            # if a target is needed, get it, randomly. The target is the place on the
            # # paddle that the paddle moves to try and hit with the ball
            if canvas.data["needTarget"]:
                ballTarget = random.randint(-int(paddleWidth - marginOfError), int(paddleWidth - marginOfError))
                canvas.data["ballTarget"] = ballTarget            

            # move the paddle
            if horizontalPaddleCenter != ballCenterX + ballTarget:

                # allows for a margin of error. in this case the range is based on
                # # the center of the paddle
                if -marginOfError < horizontalPaddleCenter - ballCenterX - ballTarget < marginOfError:
                    pass # if the ball is within the range, do nothing!

                # move the paddle if the ball is not in the range
                elif horizontalPaddleCenter > ballCenterX + ballTarget:
                    canvas.data["horizontalCenterPaddle"] -= paddleVelocity

                # move the paddle if the ball is not in the range
                elif horizontalPaddleCenter < ballCenterX + ballTarget:
                    canvas.data["horizontalCenterPaddle"] += paddleVelocity

            # next time this is called, it will not get a new target.
            canvas.data["needTarget"] = False

## CONGRADULATE a winner: takes "canvas", returns None
def winner(canvas):

    # extract information from the dictionary
    largeTextSize = canvas.data["largeTextSize"]

    # compute/initialize variables
    centerX = canvas.data["canvasWidth"] / 2
    centerY = canvas.data["canvasHeight"] / 2

    # blinks "WINNER" a few times while the score is increased 1000 points
    # # for winning
    if canvas.data["delayCounter"] < 200:
        canvas.data["delayCounter"] += 1

        if canvas.data["delayCounter"] % 36 < 18:
            canvas.create_text(centerX, centerY,
                               text = "WINNER",
                               font = ("Helvetica", largeTextSize))
        canvas.data["points"] += 5

    # this keeps blinking "WINNER" while adding 100 points for ever life
    # # retained in the course of winning
    elif canvas.data["lives"] > 0:
        
        canvas.data["delayCounter"] += 1
        if canvas.data["delayCounter"] % 36 < 18:
            canvas.create_text(centerX, centerY,
                               text = "WINNER",
                               font = ("Helvetica", largeTextSize))
            
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
    maxPaddleWidth = canvas.data["canvasWidth"] / 4

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
    canvas.data["ballCenterX"] = canvas.data["canvasWidth"] / 2
    canvas.data["ballCenterY"] = canvas.data["canvasHeight"] / 2
    canvas.data["splashScreen"] = False
    canvas.data["winner"] = False
    canvas.data["paused"] = True

## CLICK the splash screen: takes "canvas" and "event", returns None
## # this function deals with all of the events that have to do with the
## # # splash screen.  It takes you thdef splashScreenClickrough the menus of the splash screen,
## # # # changes the color of the background when it is clicked and speeds
## # # # # up the ball whenever the creator's name is clicked.
def splashScreenClick(canvas, event):

    # extract information from the canvas
    # # button
    buttonSize = canvas.data["buttonSize"]
    buttonMargin = canvas.data["buttonMargin"]

    # # canvas
    canvasHeight = canvas.data["canvasHeight"]
    canvasWidth = canvas.data["canvasWidth"]

    # # screens
    playGameScreen = canvas.data["playGameScreen"]
    instructionScreen = canvas.data["instructionScreen"]
    gameOverScreen = canvas.data["gameOverScreen"]
    highScoreScreen = canvas.data["highScoreScreen"]

    # # highscores
    writeHighScores = canvas.data["writeHighScores"]
    fileName = canvas.data["highScoreFileName"]
    

    # compute and initialize variables
    clickButtonSize = buttonSize - buttonMargin
    marginX = canvasWidth / 20
    marginY = canvasHeight / 20
    centerX = canvasWidth / 2

        
    # this is only triggered if the "hard" button is pressed on the play game screen
    if ((centerX - clickButtonSize) < event.x < (centerX + clickButtonSize)) and \
       (((marginY * 7) + buttonMargin) < event.y < ((marginY * 9) - buttonMargin)):
        if playGameScreen:

            getGameReady(canvas)
            canvas.data["difficulty"] = "hard"
            canvas.data["pointsPerHit"] = 3
            canvas.data["ballVelocityY"] = canvas.data["canvasWidth"] / 55
            timerFired(canvas)

        elif highScoreScreen:
            canvas.data["writeHighScores"] = True
            canvas.data["difficulty"] = "hard"
            getHighScores(canvas, "hard" + fileName)



    # this button is the "Play Game" button on the main screen and the "normal"
    # # button on the play game screen
    elif ((centerX - clickButtonSize) < event.x < (centerX + clickButtonSize)) and \
       (((marginY * 10) + buttonMargin) < event.y < ((marginY * 12) - buttonMargin)):
        if playGameScreen:
            
            getGameReady(canvas)
            canvas.data["difficulty"] = "normal"
            canvas.data["pointsPerHit"] = 2
            canvas.data["ballVelocityY"] = canvas.data["canvasWidth"] / 70

            timerFired(canvas)
            
        elif highScoreScreen:
            
            canvas.data["writeHighScores"] = True
            canvas.data["difficulty"] = "normal"
            
            getHighScores(canvas, "normal" + fileName)
            
        elif not (instructionScreen or gameOverScreen):
            
            canvas.data["playGameScreen"] = True
            
        else:
            
            canvas.data["splashScreenColor"] = splashScreenColor(canvas)
                      
    # this button is the "Intructions" button on the main screen and the "easy"
    # # button on the play game screen
    elif ((centerX - clickButtonSize) < event.x < (centerX + clickButtonSize)) and \
       (((marginY * 13) + buttonMargin) < event.y < ((marginY * 15) - buttonMargin)):

        if playGameScreen:
            
            getGameReady(canvas)
            canvas.data["difficulty"] = "easy"
            canvas.data["pointsPerHit"] = 1
            canvas.data["ballVelocityY"] = canvas.data["canvasWidth"] / 85

            timerFired(canvas)
            
        elif gameOverScreen:
            
            canvas.data["gameOverScreen"] = False
            resetHighScores(canvas)
            canvas.data["highScoreScreen"] = True
            canvas.data["writeHighScores"] = True
            
        elif highScoreScreen:
            
            canvas.data["writeHighScores"] = True
            canvas.data["difficulty"] = "easy"
            
            getHighScores(canvas, "easy" + fileName)
            
        elif (not gameOverScreen) and (not instructionScreen) and \
             (not gameOverScreen):
            
            canvas.data["instructionScreen"] = True
            
        else:
            
            canvas.data["splashScreenColor"] = splashScreenColor(canvas)
        
    # this button is the "High Score" button on the main screen and the "Return to
    # # main screen" button on the "Play Game," "Instructions" and "HighScores" screens
    elif ((centerX - clickButtonSize) < event.x < (centerX + clickButtonSize)) and \
       (((marginY * 16) + buttonMargin) < event.y < ((marginY * 18) - buttonMargin)):
        
        if playGameScreen: canvas.data["playGameScreen"] = False

        elif highScoreScreen and writeHighScores: canvas.data["writeHighScores"] = False

        elif highScoreScreen: canvas.data["highScoreScreen"] = False

        elif instructionScreen: canvas.data["instructionScreen"] = False

        elif gameOverScreen:
            
            canvas.data["gameOverScreen"] = False
            resetHighScores(canvas)
            
        else: canvas.data["highScoreScreen"] = True

    # if the creators name is clicked on the main splash screen it increases the speed of the
    # # ball. There is a limit, however, to how fast the ball can go.  Five clicks is the
    # # # maximum
    elif ((centerX - buttonSize) < event.x < (centerX + buttonSize)) and \
        ((( marginY * 9) - buttonMargin) < event.y < ((marginY * 9) + buttonMargin)) and \
        (not playGameScreen) and (not instructionScreen) and (not highScoreScreen):

        canvas.data["fastCounter"] += 1
        
        if canvas.data["fastCounter"] <= 5: redrawAll(canvas)
            
    # change the color of the background       
    else: canvas.data["splashScreenColor"] = splashScreenColor(canvas)
        
## MOUSE pressed: takes "event", returns None
## # this function deals with all the events that happen when the mouse
## # # is pressed
def mousePressed(event):

    # initialize variables
    canvas = event.widget.canvas
    outsideMargin = canvas.data["outsideMargin"]
    outsideMargin = outsideMargin * .75

    # if the splashscreen is up, call helper function
    if canvas.data["splashScreen"]: splashScreenClick(canvas, event)

    # this is the code that initializes the AI
    elif canvas.data["playGameScreen"] and \
         0 < event.x < outsideMargin and \
         0 < event.y < outsideMargin:
        
        canvas.data["ai"] = True
        
        ai(canvas)

        
## TYPE name: takes "canvas" and "event", returns None
## # this is a helper function for keyPressed so that when the user is typing
## # # their name they can only use letters, numbers, the backspace and the space
def typeName(canvas, event):

    # extract information from the canvas
    name = canvas.data["name"]

    # if they've hit a button, erase the current name
    if name == "Type name please.": name = ""

    # make sure the character is ok
    if ("!" < event.char < "z") and (len(name) <= 8) and (event.char != "-"): name += event.char

    # allow for backspaces
    elif event.keysym == "BackSpace": name = name[:-1]

    # allow for spaces
    elif event.keysym == "space" and len(name) <= 8: name += " "

    # set the name
    canvas.data["name"] = name
    
## KEY pressed: takes "event", returns None
## # this function deals with all of the events taht happen when the keyboard
## # # is pressed
def keyPressed(event):

    # initialize variable
    canvas = event.widget.canvas


    # extract information from the canvas
    canvasWidth = canvas.data["canvasWidth"]
    turnOver = canvas.data["turnOver"]
    paused = canvas.data["paused"]
    splashScreen = canvas.data["splashScreen"]
    win = canvas.data["winner"]
    gameOverScreen = canvas.data["gameOverScreen"]
    ai = canvas.data["ai"]

    # this code is in place for when the AI is in control.
    # # this disables the AI
    if not gameOverScreen and not win:
        if event.keysym == "q" or event.keysym == "Q":
            canvas.data["ai"] = False
        elif event.keysym == "space":
            canvas.data["ai"] = False

    # if the AI is not in control, go ahead and allow the user to type
    if not ai:
        # go to a helper funtion if it's the gameOverScreen. This is where the
        # # user types his/her name
        if canvas.data["gameOverScreen"] == True:
            typeName(canvas, event)
        
        else: 
            # moves top and bottom paddles to the left
            if event.keysym == "Left" and not turnOver:
                canvas.data["horizontalPaddleVelocity"] = canvasWidth / 70
                canvas.data["horizontalPaddleVelocity"] -= (canvas.data["horizontalPaddleVelocity"] * 2)

            # moves top and bottom paddles to the right
            elif event.keysym == "Right" and not turnOver:
                canvas.data["horizontalPaddleVelocity"] = canvasWidth / 70
                canvas.data["horizontalPaddleVelocity"] = abs(canvas.data["horizontalPaddleVelocity"])

            # moves left and rights paddles down
            elif event.keysym == "Down" and not turnOver:
                canvas.data["verticalPaddleVelocity"] = canvasWidth / 70
                canvas.data["verticalPaddleVelocity"] = abs(canvas.data["verticalPaddleVelocity"])

            # moves left and right paddles up
            elif event.keysym == "Up" and not turnOver:
                canvas.data["verticalPaddleVelocity"] = canvasWidth / 70
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
        canvas.data["buttonColor1"] = "white"
        canvas.data["buttonColor2"] = "white"
        canvas.data["buttonColor3"] = "white"
        canvas.data["buttonSize"] = canvas.data["canvasWidth"] / 10
        canvas.data["buttonMargin"] = canvas.data["buttonSize"] - (canvas.data["canvasWidth"] / 11)

        # ball
        canvas.data["splashColorOfBall"] = "white"
        canvas.data["splashRadius"] = canvas.data["canvasWidth"] / 20
        canvas.data["splashBallVX"] = 0
        canvas.data["splashBallVY"] = canvas.data["canvasWidth"] / 50

        # current screen
        canvas.data["splashScreen"] = True
        canvas.data["instructionScreen"] = False
        canvas.data["playGameScreen"] = False
        canvas.data["highScoreScreen"] = False
        canvas.data["writeHighScores"] = False
        canvas.data["splashScreenColor"] = "white"

        # misc
        canvas.data["fastCounter"] = 0
        canvas.data["splashDelay"] = 30
        canvas.data["delayCounter"] = 0
        canvas.data["pausedCounter"] = 0
        canvas.data["name"] = "Type name please."

    ## UNIVERSAL INFORMATION: takes nothing, returns None,
    ## # but saves the information in the dictionary
    def universalInit():
        # ball
        canvas.data["ballCenterX"] = canvas.data["canvasWidth"] / 2
        canvas.data["ballCenterY"] = canvas.data["canvasHeight"] / 2

        # all moving objects
        canvas.data["borderWidth"] = canvas.data["canvasWidth"] / 350

        # text
        canvas.data["smallTextSize"] = canvas.data["canvasWidth"] / 35
        canvas.data["mediumSmallTextSize"] = canvas.data["canvasWidth"] / 28
        canvas.data["mediumLargeTextSize"] = canvas.data["canvasWidth"] / 20
        canvas.data["largeTextSize"] = canvas.data["canvasWidth"] / 10

        # url / filename
        canvas.data["dateUrl"] = "http://tycho.usno.navy.mil/cgi-bin/timer.pl"
        canvas.data["highScoreFileName"] = "_high_scores.txt"
        
    ## AI INFORMATION: takes nothing, returns None,
    ## # but saves the information in the dictionary
    def aiInit():
        canvas.data["aiCounter"] = 0
        canvas.data["needTarget"] = True
        canvas.data["ballTarget"] = 0
        canvas.data["aiName"] = [".", "I", ".", "A"]
        canvas.data["aiMessage"] = ["!","g","n","i","y","a","l","p"," ",
                                    "r","o","f"," ",
                                    "s", "k", "n", "a", "h", "T"]
        
        
    ## GAMEPLAY INFORMATION: takes nothing, returns None,
    ## # but saves the information in the dictionary
    def gameInit():
        # paddles
        canvas.data["horizontalCenterPaddle"] = canvas.data["canvasWidth"] / 2
        canvas.data["verticalCenterPaddle"] = canvas.data ["canvasWidth"] / 2
        canvas.data["horizontalPaddleVelocity"] = 0
        canvas.data["verticalPaddleVelocity"] = 0
        canvas.data["paddleWidth"] = canvas.data["canvasWidth"] / 6
        canvas.data["paddleHeight"] = canvas.data["canvasWidth"] / 50
        canvas.data["paddleColor"] = "black"
        
        # ball
        canvas.data["radius"] = canvas.data["canvasWidth"] / 60
        canvas.data["ballVelocityX"] = canvas.data["canvasWidth"] / 400
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
        canvas.data["outsideMargin"] = canvas.data["canvasWidth"] / 20

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
            for row in xrange(rows):
                blockGrid += [[False] * columns]
                colorGrid += [[None] * columns]

            def getColor(row, column):
                while True:
                    color = random.choice(colors)
                    if color != colorGrid[row - 1][column] and \
                       color != colorGrid[row][column - 1]:
                        return color
            # randomize the colors for all of the cells
            for row in xrange(1, rows - 1):
                for column in xrange(1, columns - 1):
                    colorGrid[row][column] = getColor(row, column)
                    
                    
            return (blockGrid, colorGrid)

        ## LEVEL ONE: takes nothing, returns level's boolean/color grids
        ## # this function makes level one
        def makeLevelOne():

            # initialize variables
            (blockGrid,colorGrid) = makeBlankLevel()

            # set certain blocks to True
            for row in xrange(5, 10):
                for column in xrange(1,4):
                    blockGrid[row][column] = True

            return (blockGrid, colorGrid)

        ## LEVEL TWO: takes nothing, returns level's boolean/color grids
        ## # this function makes level two
        def makeLevelTwo():

            # initialize variables
            (blockGrid,colorGrid) = makeBlankLevel()

            # set certain blocks to True
            for row in xrange(3, 15):
                blockGrid[row][1] = True
                    
            for row in xrange(3, 15):
                blockGrid[row][3] = True
                    
            return (blockGrid, colorGrid)

        ## LEVEL THREE: takes nothing, returns level's boolean/color grids
        ## # this funciton makes level three
        def makeLevelThree():

            # initialize variables
            (blockGrid,colorGrid) = makeBlankLevel()

            # set certain blocks to True
            for row in xrange(3, 9):
                blockGrid[row][1] = True

            for row in xrange(3, 9):
                blockGrid[row][3] = True
                    
            for row in xrange(13, 19):
                blockGrid[row][1] = True
                
            for row in xrange(13, 19):
                blockGrid[row][3] = True

            return (blockGrid, colorGrid)

        ## LEVEL FOUR: takes nothing, returns level's boolean/color grids
        ## # this function makes level four
        def makeLevelFour():

            # initialize variables
            (blockGrid,colorGrid) = makeBlankLevel()

            # set certain blocks to True
            for row in xrange(3, 17, 2):
                for column in xrange(1, 4, 2):
                    blockGrid[row][column] = True
                    
            for row in xrange(4, 16, 2):
                for column in xrange(2, 4, 2):
                    blockGrid[row][column] = True

            return (blockGrid, colorGrid)

        ## LEVEL FIVE: takes nothing, returns level's boolean/color grids
        ## # this function makes level five
        def makeLevelFive():

            # initialize variables
            (blockGrid,colorGrid) = makeBlankLevel()

            # set certain blocks to True
            for row in xrange(3, 15):
                blockGrid[row][1] = True
                    
            for row in xrange(3, 15):
                blockGrid[row][3] = True
                    
            for row in xrange(3, 7):
                blockGrid[row][2] = True
                    
            for row in xrange(11, 15):
                blockGrid[row][2] = True

            return (blockGrid, colorGrid)

        ## LEVEL SIX: takes nothing, returns level's boolean/color grids
        ## # this function makes level six
        def makeLevelSix():

            # initialize variables
            (blockGrid,colorGrid) = makeBlankLevel()
            trueFalse = [True, False]

            # set certain blocks to True, randomly
            for row in xrange(3, 15):
                for column in xrange(1, 4):
                    blockGrid[row][column] = random.choice(trueFalse)

            return (blockGrid, colorGrid)

        ## LEVEL SEVEN: takes nothing, returns level's boolean/color grids
        ## # this function makes level seven
        def makeLevelSeven():

            # initialize variables
            (blockGrid,colorGrid) = makeBlankLevel()

            # set certain blocks to True
            for row in xrange(3, 15):
                blockGrid[row][1] = True
                
            for row in xrange(3, 15):
                blockGrid[row][3] = True

            for row in xrange(3, 5):
                blockGrid[row][2] = True
                    
            for row in xrange(8, 10):
                blockGrid[row][2] = True
                
            for row in xrange(13, 15):

                blockGrid[row][2] = True

            return (blockGrid, colorGrid)

        ## LEVEL EIGHT: takes nothing, returns level's boolean/color grids
        ## # this function makes level eight
        def makeLevelEight():
            
            # initialize variables
            (blockGrid,colorGrid) = makeBlankLevel()

            # set certain blocks to True
            for row in xrange(3, 18):
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
            for row in xrange(3, 20):
                for column in xrange(1, 4):
                    blockGrid[row][column] = True

            for row in xrange(16, 20):
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
            for row in xrange(rows):
                blockGrid += [[False] * columns]

            return blockGrid
        
        # blocks
        canvas.data["rows"] = 35
        canvas.data["columns"] = 5
        canvas.data["rowStep"] = canvas.data["canvasWidth"] / 30
        canvas.data["columnStep"] = canvas.data["canvasWidth"] / 5
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
    aiInit()
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
    textSize = canvas.data["mediumLargeTextSize"]
    lives = canvas.data["lives"]

    # compute / intitialize variables
    centerX = canvas.data["canvasWidth"] / 2
    centerY = canvas.data["canvasHeight"] /2

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
                           font = ("Helvetica", textSize))
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
    canvas.data["horizontalCenterPaddle"] = canvas.data["canvasWidth"] / 2
    canvas.data["verticalCenterPaddle"] = canvas.data ["canvasWidth"] / 2
    canvas.data["horizontalPaddleVelocity"] = 0
    canvas.data["verticalPaddleVelocity"] = 0
    canvas.data["paddleColor"] = "black"

    # ball
    canvas.data["ballCenterX"] = canvas.data["canvasWidth"] / 2
    canvas.data["ballCenterY"] = canvas.data["canvasHeight"] / 2
    canvas.data["ballVelocityX"] = canvas.data["canvasWidth"] / 400
    canvas.data["ballColorCounter"] = 0

    # set the speed of the ball according to the difficulty level
    if difficulty == "hard":
        canvas.data["ballVelocityY"] = canvas.data["canvasWidth"] / 55
    elif difficulty == "normal":
         canvas.data["ballVelocityY"] = canvas.data["canvasWidth"] / 70
    elif difficulty == "easy":
          canvas.data["ballVelocityY"] = canvas.data["canvasWidth"] / 85    

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
    if playGameScreen: canvas.after(delay, timerFired, canvas)

##### END CONTROL CENTER #####
##############################

## RUN the program
## # this function starts the program running
def run():

    # intialize variables
    canvasWidth = 700
    canvasHeight = canvasWidth
    
    # initialize canvas
    root = Tk()
    canvas = Canvas(root, width=canvasWidth, height= canvasHeight, background="white")
    canvas.pack()

    # make it so the window is not resizable
    root.resizable(height = 0, width = 0)

    # give the canvas a title
    root.title("BLOCK BUSTER!")

    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas

    # set up dicitonary
    canvas.data = { }

    # store values in the dictionary that will not need to be reset
    # # when most else needs to be.  These variables will be changed
    # # # in the code as needed
    canvas.data["canvasWidth"] = canvasWidth
    canvas.data["canvasHeight"] = canvasHeight
    canvas.data["lastGamePoints"] = 0
    canvas.data["gameOverScreen"] = False
    canvas.data["difficulty"] = None
    canvas.data["winner"] = False
    canvas.data["ai"] = False

    # sets up events
    root.bind("<Key>", keyPressed)
    root.bind("<Button-1>", mousePressed)

    # let the games begin
    init(canvas)
    canvas.data["date"] = getDate(canvas.data["dateUrl"])
    redrawAll(canvas)
    
    # This call BLOCKS (so your program waits until you close the window!)
    root.mainloop()
    
run()
