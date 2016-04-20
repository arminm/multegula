# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# PauseScreen.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
from UI.typedefs import *

# PausedScreen - this will be placed over top of a game screen
class PauseScreen :
    ### __init__ - initialize and return a PauseScreen
    def __init__(self) :
        self.counter = 0
        self.first = True
        self.text = '3'

    ### reset -- resets the screen data
    def reset(self, canvas) :
        canvas.delete(self.tLevel)
        canvas.delete(self.tSub)
        canvas.delete(self.tCountdown)
        self.counter = 0  
        self.text = '3' 

    ### count - count the number of times this has been drawn to change the color of the blocks
    def count(self, canvas) :
        # counter - 
        #   - use to display 3 - 2 - 1 countdown
        #   - use to move to next screen after pause is complete
        if canvas.data['gameType'] == GameType.SINGLE_PLAYER :
            if(self.counter == DISP_3_VAL) :
                self.text = '3'
                status = PauseReturnStatus.DISP_3
            if(self.counter == DISP_2_VAL) :
                self.text = '2'
                status = PauseReturnStatus.DISP_2
            elif(self.counter == DISP_1_VAL) :
                self.text = '1'
                status = PauseReturnStatus.DISP_1
            elif(self.counter == MOVE_ON_VAL) : 
                status = PauseReturnStatus.MOVE_ON
            else :
                status = PauseReturnStatus.NO_STATUS
        elif canvas.data['gameType'] == GameType.MULTI_PLAYER :
            if(self.counter == DISP_3_VAL) :
                status = PauseReturnStatus.DISP_3
            if(self.counter == DISP_2_VAL) :
                status = PauseReturnStatus.DISP_2
            elif(self.counter == DISP_1_VAL) :
                status = PauseReturnStatus.DISP_1
            elif(self.counter == MOVE_ON_VAL) : 
                status = PauseReturnStatus.MOVE_ON
            else :
                status = PauseReturnStatus.NO_STATUS            

        # increment counter
        self.counter += 1
        return status


    ### setScreen - set the screen in the canvas
    def setScreen(self, canvas) : 
        # print the pause screen text
        self.tLevel = canvas.create_text(X_CENTER, Y_THIRD, text = canvas.data['level'].getTextLevel(),
                                        font = ('Courier', XL_TEXT_SIZE))

        self.tSub = canvas.create_text(X_CENTER, Y_CENTER, text = 'Starting in...',
                                        font = ('Courier', L_TEXT_SIZE))

        self.tCountdown = canvas.create_text(X_CENTER, Y_2THIRD, text = self.text,
                                        font = ('Courier', XL_TEXT_SIZE), fill = 'black')  

    ### draw - manages the drawing of this screen
    def draw(self, canvas) :
        status = PauseReturnStatus.NO_STATUS

        # Single player game -> increment the counter
        if canvas.data['gameType'] == GameType.SINGLE_PLAYER :
            status = self.count(canvas)

        # Multiplayer game -> check the unicorn
        elif canvas.data['gameType'] == GameType.MULTI_PLAYER :
            iam = canvas.data['myName']
            unicorn = canvas.data['unicorn']

            # if I am the unicorn -> increment the counter
            if iam == unicorn :
                status = self.count(canvas)

        # either reset or draw based on the return status of count()
        if status == PauseReturnStatus.MOVE_ON :
            self.reset(canvas)
        elif not(self.first) :
            canvas.delete(self.tLevel)
            canvas.delete(self.tSub)
            canvas.delete(self.tCountdown)
            self.setScreen(canvas)
        elif self.first :
            self.setScreen(canvas)
            self.first = False
        
        return status

