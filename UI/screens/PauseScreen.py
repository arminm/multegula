# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# PauseScreen.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
from UI.components.ComponentDefs import *
from UI.screens.ScreenEnum import *

# PausedScreen - this will be placed over top of a game screen
class PauseScreen :
    ### __init__ - initialize and return a PauseScreen
    def __init__(self) :
        self.color1 = 'black'
        self.color2 = 'grey'
        self.color3 = 'grey'
        self.counter = 0
        self.first = True

    ### reset -- resets the screen data
    def reset(self, canvas) :
        canvas.delete(self.tLevel)
        canvas.delete(self.tSub)
        canvas.delete(self.t3)
        canvas.delete(self.t2)
        canvas.delete(self.t1)
        self.counter = 0
        self.color1 = 'black'
        self.color2 = 'grey'
        self.color3 = 'grey'     

    ### count - count the number of times this has been drawn to change the color of the blocks
    def count(self, canvas) :
        # counter - 
        #   - use to display 3 - 2 - 1 countdown
        #   - use to move to next screen after pause is complete
        self.counter += 1
        if(self.counter == 50) :
            self.color1 = 'grey'
            self.color2 = 'black'
            self.color3 = 'grey'

        elif(self.counter == 100) :
            self.color1 = 'grey'
            self.color2 = 'grey'
            self.color3 = 'black'

        elif(self.counter == 150) : 
            canvas.data['currentScreen'] = canvas.data['nextScreen']
            canvas.data['nextScreen'] = Screens.SCRN_NONE
            self.reset(canvas)

    ### setScreen - set the screen in the canvas
    def setScreen(self, canvas) : 
        color1 = self.color1
        color2 = self.color2
        color3 = self.color3

        # print the pause screen text
        self.tLevel = canvas.create_text(X_CENTER, Y_THIRD, text = canvas.data['level'].getTextLevel(),
                                        font = ('Courier', XL_TEXT_SIZE))

        self.tSub = canvas.create_text(X_CENTER, Y_CENTER, text = 'Starting in...',
                                        font = ('Courier', L_TEXT_SIZE))

        self.t3 = canvas.create_text(X_THIRD, Y_2THIRD, text = '3',
                                        font = ('Courier', XL_TEXT_SIZE), fill = color1)  

        self.t2 = canvas.create_text(X_CENTER, Y_2THIRD, text = '2', 
                                        font = ('Courier', XL_TEXT_SIZE), fill = color2)

        self.t1 = canvas.create_text(X_2THIRD, Y_2THIRD, text = '1',
                                        font = ('Courier', XL_TEXT_SIZE), fill = color3)

    ### draw - manages the drawing of this screen
    def draw(self, canvas) :
        if(not(self.first)) :
            canvas.delete(self.tLevel)
            canvas.delete(self.tSub)
            canvas.delete(self.t3)
            canvas.delete(self.t2)
            canvas.delete(self.t1)
            self.setScreen(canvas)
        elif(self.first) :
            self.setScreen(canvas)
            self.first = False
        
        self.count(canvas)


