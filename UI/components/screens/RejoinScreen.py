# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# RejoinScreen.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
from UI.typedefs import *

# RejoinScreen - this will be placed over top of a game screen
class RejoinScreen :
    ### __init__ - initialize and return a PauseScreen
    def __init__(self) :
        self.counter = 0
        self.first = True
        self.text = 'Hang tight while we sync up.'

    ### reset -- resets the screen data
    def reset(self, canvas) :
        canvas.delete(self.tLevel)
        canvas.delete(self.tSub)
        canvas.delete(self.tCountdown)
        self.counter = 0  
        self.text = 'Hang tight while we sync up.'

    ### count - count the number of times this has been drawn to change the color of the blocks
    def count(self, canvas) :
        updated = False

        # blink the text
        if self.counter == 50 :
            self.text = ''
            updated = True
        elif self.counter == 100 :
            self.text = 'Hang tight while we sync up.'    
            self.counter = 0 
            updated = True 

        # increment counter
        self.counter += 1
        return updated

    ### setScreen - set the screen in the canvas
    def setScreen(self, canvas) : 
        # print the pause screen text
        self.tLevel = canvas.create_text(X_CENTER, Y_THIRD, text = canvas.data['level'].getTextLevel(),
                                        font = ('Courier', XL_TEXT_SIZE))

        self.tSub = canvas.create_text(X_CENTER, Y_CENTER, text = 'Something went wrong...',
                                        font = ('Courier', L_TEXT_SIZE))

        self.tCountdown = canvas.create_text(X_CENTER, Y_2THIRD, text = self.text,
                                        font = ('Courier', M_TEXT_SIZE), fill = 'black')  

    ### draw - manages the drawing of this screen
    def draw(self, canvas) :
        # count and determine if the count was updated
        updated = self.count(canvas)

        # either reset or draw based on the return status of count()
        if not(self.first) and updated:
            canvas.delete(self.tLevel)
            canvas.delete(self.tSub)
            canvas.delete(self.tCountdown)
            self.setScreen(canvas)
        elif self.first :
            self.setScreen(canvas)
            self.first = False
