# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# Player.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
from enum import Enum
import random
from UI.typedefs import *
from UI.components.gameplay.Paddle import *

# PLAYER class
class Player :
    ### __init__  - initialize and return Player
    ##  @param orientation - location on the screen of this padde (DIR_NORTH/DIR_SOUTH/...)
    ##  @param state - current control state of the player (USER/AI/COMP)
    def __init__(self, orientation, state, name, gameType) :
        self.ORIENTATION = orientation
        self.state = state
        self.score = 0
        self.lives = INIT_LIVES
        self.power = PowerUps.PWR_NONE
        self.paddle = Paddle(orientation, state, gameType)
        self.first = True
        self.statusUpdate = False
        self.dead = False
        self.name = name
        self.gameType = gameType
        self.levelOrientation = Orientation.DIR_SOUTH;

    ### iAmDead 
    ##  Set the appropriate fields to make this player dead
    def iAmDead(self) :
        self.state = PlayerState.DEAD
        self.paddle.iAmDead() 
        self.dead = True

    ### getStatus 
    ##  Return the status of the player (score, lives, power)
    def getStatus(self) :
        return (self.name, self.state, self.score, self.lives, self.power)

    ### AI method -
    ##  This method moves the paddles automatically to contact the ball. There are some
    ##  non-idealities built in so the computer is not perfect
    def AI(self, canvas) :
        # get ball/paddle information
        (ballCenterX, ballCenterY, ballRadius) = canvas.data['ball'].getInfo()
        (paddleCenter, paddleWidth, paddleDir, paddleOrientation) = self.paddle.getInfo()

        # calcualte an offset and a random number - used to create a delay in the paddle response
        offset = paddleWidth // 5
        chance = random.randint(0, 4)

        # determine which direction the ball in from the center of the paddle based on the
        #   current orientation.
        if paddleOrientation == Orientation.DIR_NORTH or paddleOrientation == Orientation.DIR_SOUTH :
            direction = paddleCenter - ballCenterX
        elif paddleOrientation == Orientation.DIR_WEST or paddleOrientation == Orientation.DIR_EAST :
            direction = paddleCenter - ballCenterY

        # MOVE the paddle -
        ## if the ball has moved at least 'offset' distance from the center of the paddle, 
        ##  the paddle is currently stopped, and it's your lucky day -> move the paddle
        if((abs(direction) > offset) and (paddleDir == Direction.DIR_STOP) and (chance == 1)) : 
            if(direction < offset) :
                self.paddle.direction = Direction.DIR_RIGHT
            elif direction > offset :
                self.paddle.direction = Direction.DIR_LEFT

        ## otherwise, if it's your lucky day -> stop the paddle
        elif chance == 0 :
            self.paddle.direction = Direction.DIR_STOP

    ### deflectBall method - 
    ##  Check to see if the ball is off the playing field or is being deflected by the player's paddle.
    def deflectBall(self, canvas) :
        # get canvas/paddle/ball info
        orientation = self.ORIENTATION
        (ballLeft, ballRight, ballTop, ballBottom) = canvas.data['ball'].getEdges()
        (paddleLeft, paddleRight, paddleTop, paddleBottom) = self.paddle.getEdges()
        (paddleCenter, paddleWidth, paddleDir, paddleOrientation) = self.paddle.getInfo()
        myState = self.state

        # initialize flags
        ballMissed = False
        ballDeflected = False

        # NORTH paddle
        if orientation == Orientation.DIR_NORTH :
            if (X_LIMIT_MIN <= ballRight) and (ballLeft <= X_LIMIT_MAX) and (ballBottom <= 0) :
                ballMissed = True
            elif (paddleLeft <= ballRight) and (ballLeft <= paddleRight) and (paddleTop < ballTop <= paddleBottom) :
                ballDeflected = True
        # SOUTH paddle
        elif orientation == Orientation.DIR_SOUTH :
            if (X_LIMIT_MIN <= ballRight) and (ballLeft <= X_LIMIT_MAX) and (CANVAS_HEIGHT <= ballTop) :
                ballMissed = True
            elif (paddleLeft <= ballRight) and (ballLeft <= paddleRight) and (paddleTop <= ballBottom < paddleBottom) :
                ballDeflected = True
        # EAST paddle
        elif orientation == Orientation.DIR_EAST :
            if (Y_LIMIT_MIN <= ballTop) and (ballBottom <= Y_LIMIT_MAX) and (CANVAS_WIDTH <= ballLeft) :
                ballMissed = True
            elif (paddleTop <= ballBottom) and (ballTop <= paddleBottom) and (paddleLeft <= ballRight < paddleRight) :
                ballDeflected = True
        # WEST paddle
        elif orientation == Orientation.DIR_WEST :
            if (Y_LIMIT_MIN <= ballTop) and (ballBottom <= Y_LIMIT_MAX) and (ballRight <= 0) :
                ballMissed = True
            elif (paddleTop <= ballBottom) and (ballTop <= paddleBottom) and (paddleLeft < ballLeft <= paddleRight) :
                ballDeflected = True

        # set return status bassed on player type and 
        if myState == PlayerState.WALL :
            if ballDeflected :
                return (PlayerReturnStatus.WALL_BALL_DEFLECTED, self.deflectBallVelocity(canvas))
            return (PlayerReturnStatus.WALL_NO_STATUS, [])

        elif myState == PlayerState.DEAD :
            if ballDeflected :
                return (PlayerReturnStatus.DEAD_BALL_DEFLECTED, self.deflectBallVelocity(canvas))
            return (PlayerReturnStatus.DEAD_NO_STATUS, [])

        else :
            if ballMissed :
                return (PlayerReturnStatus.BALL_MISSED, [])
            elif ballDeflected :
                return (PlayerReturnStatus.BALL_DEFLECTED, self.deflectBallVelocity(canvas))
            return (PlayerReturnStatus.NO_STATUS, [])

    ### deflectBallVelocity - 
    ##  Deflect ball off of a paddle and determine the new direction off the ball
    def deflectBallVelocity(self, canvas) :
        # initialize speed and random offset variables
        speed = BALL_SPEED_INIT
        offsetFactor = random.uniform(1, 1.1)
        offset = random.uniform(-0.1, 0.1)

        # get ball/paddle info
        (paddleCenter, paddleWidth, paddleDir, paddleOrientation) = self.paddle.getInfo()
        (ballCenterX, ballCenterY, ballRadius) = canvas.data['ball'].getInfo()
        (xVelocity, yVelocity) = canvas.data['ball'].getVelocity()

        # deflect off NORTH paddle
        if paddleOrientation == Orientation.DIR_NORTH :
            if self.state == PlayerState.WALL or self.state == PlayerState.DEAD :
                yVelocity = (-yVelocity)
            else :
                speedFactor = (ballCenterX - paddleCenter) / paddleWidth
                xVelocity = round(speed * speedFactor * offsetFactor + offset, RD_FACT)
                yVelocity = speed        

        # deflect off SOUTH paddle
        elif paddleOrientation == Orientation.DIR_SOUTH :
            if self.state == PlayerState.WALL or self.state == PlayerState.DEAD :
                yVelocity = (-yVelocity)
            else :
                speedFactor = (ballCenterX - paddleCenter) / paddleWidth
                xVelocity = round(speed * speedFactor * offsetFactor + offset, RD_FACT)
                yVelocity = (-speed)

        # deflect off EAST paddle
        elif paddleOrientation == Orientation.DIR_EAST :
            if self.state == PlayerState.WALL or self.state == PlayerState.DEAD :
                xVelocity = (-xVelocity)
            else :
                speedFactor = (ballCenterY - paddleCenter) / paddleWidth
                xVelocity = (-speed)
                yVelocity = round(speed * speedFactor * offsetFactor + offset, RD_FACT)
        
        # deflect off WEST paddle
        elif(paddleOrientation == Orientation.DIR_WEST) :
            if self.state == PlayerState.WALL or self.state == PlayerState.DEAD :
                xVelocity = (-xVelocity)
            else : 
                speedFactor = (ballCenterY - paddleCenter) / paddleWidth
                xVelocity = speed
                yVelocity = round(speed * speedFactor * offsetFactor + offset, RD_FACT)

        return [xVelocity, yVelocity]

    ### breakBlock --
    ##  handles the breaking of blocks
    def breakBlock(self, canvas) :
        (ballLeft, ballRight, ballTop, ballBottom) = canvas.data['ball'].getEdges()
        (ballCenterX, ballCenterY, ballRadius) = canvas.data['ball'].getInfo()
        (xVelocity, yVelocity) = canvas.data['ball'].getVelocity()
        blocks = canvas.data['level'].blocks;
        broken = False;
        returnInfo = []

        # ball moving NORTH WEST
        if xVelocity < 0 and yVelocity <= 0 :
            for blockIndex, block in enumerate(blocks) :
                if(block.enabled == True) :
                    (blkLeft, blkRight, blkTop, blkBottom) = block.getEdges(self.levelOrientation)
                    # hit bottom of the block
                    if (ballTop <= blkBottom) and (ballBottom > blkBottom) and (blkLeft <= ballRight) and (ballLeft <= blkRight) :
                        returnInfo = [xVelocity, (-yVelocity), blockIndex]
                        broken =True;
                        break
                    # hit right side of the block
                    elif (ballLeft <= blkRight) and (ballRight > blkRight) and (blkTop <= ballBottom) and (ballTop <= blkBottom) :
                        returnInfo = [(-xVelocity), yVelocity, blockIndex]
                        broken = True;
                        break                                     

        # ball moving NORTH EAST
        elif(xVelocity >= 0) and (yVelocity < 0) :
            for blockIndex, block in enumerate(blocks) :
                if(block.enabled == True) :
                    # hit bottom of the block
                    (blkLeft, blkRight, blkTop, blkBottom) = block.getEdges(self.levelOrientation)
                    if (ballTop <= blkBottom) and (ballBottom > blkBottom) and (blkLeft <= ballRight) and (ballLeft <= blkRight) :
                        returnInfo = [xVelocity, (-yVelocity), blockIndex]
                        broken = True
                        break
                    # hit left side of the block
                    elif (ballRight >= blkLeft) and (ballLeft < blkRight) and (blkTop <= ballBottom) and (ballTop <= blkBottom) :
                        returnInfo = [(-xVelocity), yVelocity, blockIndex]
                        broken = True;
                        break                                   
          
        # ball moving SOUTH WEST
        elif(xVelocity < 0) and (yVelocity >  0) :
            for blockIndex, block in enumerate(blocks) :
                if(block.enabled == True) :
                    # hit top of the block
                    (blkLeft, blkRight, blkTop, blkBottom) = block.getEdges(self.levelOrientation)
                    if (ballBottom >= blkTop) and (ballTop < blkTop) and (blkLeft <= ballRight) and (ballLeft <= blkRight) :
                        returnInfo = [xVelocity, (-yVelocity), blockIndex]
                        broken = True;
                        break
                    # hit right of the block
                    elif (ballLeft <= blkRight) and (ballRight > blkRight) and (blkTop <= ballBottom) and (ballTop <= blkBottom) :
                        returnInfo = [(-xVelocity), yVelocity, blockIndex]
                        broken = True;
                        break

        # ball moving SOUTH EAST
        elif(xVelocity >= 0) and (yVelocity > 0) :
            for blockIndex, block in enumerate(blocks) :
                if(block.enabled == True) :
                    (blkLeft, blkRight, blkTop, blkBottom) = block.getEdges(self.levelOrientation)
                    # hit top of the block
                    if (ballBottom >= blkTop) and (ballTop < blkTop) and (blkLeft <= ballRight) and (ballLeft <= blkRight) :
                        returnInfo = [xVelocity, (-yVelocity), blockIndex]
                        broken = True;
                        break
                    # hit left side of the block
                    elif (ballRight >= blkLeft) and (ballLeft < blkRight) and (blkTop <= ballBottom) and (ballTop <= blkBottom) :
                        returnInfo = [(-xVelocity), yVelocity, blockIndex]
                        broken = True;
                        break

        # if there was a broken block - return appropriate information
        if broken == True :
            return (PlayerReturnStatus.BLOCK_BROKEN, returnInfo)
        return (PlayerReturnStatus.NO_STATUS, [])

    ### detectDeadNodes -
    ##  Determine if a dead node has been detected based on the ball location
    def detectDeadNodes(self, canvas) :
        (ballCenterX, ballCenterY, ballRadius) = canvas.data['ball'].getInfo()

        #  check WEST
        if(ballCenterX < (-CANVAS_WIDTH)) :
            return (PlayerReturnStatus.BALL_OOB, [Orientation.DIR_WEST])
        # check EAST
        elif (ballCenterX > (2*CANVAS_WIDTH)) :
            return (PlayerReturnStatus.BALL_OOB, [Orientation.DIR_EAST])
        # check NORTH
        elif (ballCenterY < (-CANVAS_HEIGHT)) :
            return (PlayerReturnStatus.BALL_OOB, [Orientation.DIR_NORTH])
        # otherwise
        else : 
            return (PlayerReturnStatus.NO_STATUS, [])

    ### setStatus method -
    ##  Place the status text for the player on the canvas
    def setStatus(self, canvas) :
        # get canvas info
        ORIENTATION = self.ORIENTATION
        X_MARGIN = CANVAS_WIDTH // 60
        Y_MARGIN = CANVAS_HEIGHT // 60

        # initilize status message
        statusMsg = self.name + ' : '

        # determin X_LOC, Y_LOC, and NAME based on orientation
        if(ORIENTATION == Orientation.DIR_NORTH) :
            X_LOC = CANVAS_WIDTH*0.25
            Y_LOC = Y_MARGIN
        elif(ORIENTATION == Orientation.DIR_SOUTH) :
            X_LOC = CANVAS_WIDTH*0.75
            Y_LOC = CANVAS_HEIGHT - Y_MARGIN
        elif(ORIENTATION == Orientation.DIR_EAST) :
            X_LOC = CANVAS_WIDTH*0.75
            Y_LOC = Y_MARGIN    
        elif(ORIENTATION == Orientation.DIR_WEST) :
            X_LOC = CANVAS_WIDTH*0.25
            Y_LOC = CANVAS_HEIGHT - Y_MARGIN

        # finish status message and display
        statusMsg += 'P/' + str(self.score) + '.  L/' + str(self.lives) + '.'
        self.t = canvas.create_text(X_LOC, Y_LOC, text = statusMsg,
                                    font = ('Courier', S_TEXT_SIZE), fill = 'white')
        
    ### displayStatus method -
    ##  Display the text for the player indicating the current score and number of lives remaining
    def displayStatus(self, canvas) :
        if not(self.first) and self.statusUpdate :
            canvas.delete(self.t)
            self.setStatus(canvas)
            self.statusUpdate = False
        elif(self.first) :
            self.setStatus(canvas)
            self.first = False

    ### general purpose update
    def update(self, canvas) :
        # initialze return status to NONE
        returnStatus = PlayerReturnStatus.NO_STATUS

        if self.state != PlayerState.WALL :
            self.displayStatus(canvas)

        if self.lives == 0 and self.dead == False:
            self.iAmDead()

        # if this is an AI, then updae the motion of the paddles via the AI routine
        if self.state == PlayerState.AI :
            self.AI(canvas)

        # update player for motion and deflection
        #if self.state == PlayerState.USER or self.state == PlayerState.AI or self.state == PlayerState.WALL or self.:
        if self.state != PlayerState.COMP :
            # update the paddle
            self.paddle.update(canvas)
            (status, payload) = self.deflectBall(canvas)

            # if the ball hasn't been deflected or missed, determine if a block has been broken
            if status == PlayerReturnStatus.NO_STATUS and canvas.data['ball'].lastToTouch == self.name :
                (status, payload) = self.breakBlock(canvas)

            # if the ball hasn't been deflected, missed, and a block hasn't been broken, check to see if 
            ##  another node has missed the ball
            if status == PlayerReturnStatus.NO_STATUS :
                (status, payload) = self.detectDeadNodes(canvas)

            # return information to the UI
            return (status, payload)

        # if this player is a competitor, just draw it
        elif self.state == PlayerState.COMP :
            self.paddle.update(canvas)
            return (PlayerReturnStatus.NO_STATUS, [])


