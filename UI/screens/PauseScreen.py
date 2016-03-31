# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# PauseScreen.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
from screens.ScreenEnum import *

# PausedScreen - this will be placed over top of a game screen
class PauseScreen :
    ### __init__ - initialize and return a PauseScreen
    ##  @param canvas_width
    ##  @param canvas_height
    def __init__(self, canvas_width, canvas_height) :
        self.CANVAS_WIDTH = canvas_width
        self.CANVAS_HEIGHT = canvas_height
        self.X_CENTER  = canvas_width // 2
        self.X_1_THIRD = canvas_width * 0.33
        self.X_2_THIRD = canvas_width * 0.66
        self.Y_CENTER  = canvas_height // 2
        self.Y_1_THIRD = canvas_height * 0.33
        self.Y_2_THIRD = canvas_height * 0.66
        self.color1 = "black"
        self.color2 = "grey"
        self.color3 = "grey"
        self.counter = 0
        self.first = True

    def reset(self, canvas) :
        canvas.delete(self.tLevel)
        canvas.delete(self.tSub)
        canvas.delete(self.t3)
        canvas.delete(self.t2)
        canvas.delete(self.t1)
        self.counter = 0
        self.color1 = "black"
        self.color2 = "grey"
        self.color3 = "grey"     

    def count(self, canvas) :
        # counter - 
        #   - use to display 3 - 2 - 1 countdown
        #   - use to move to next screen after pause is complete
        self.counter += 1
        if(self.counter == 50) :
            self.color1 = "grey"
            self.color2 = "black"
            self.color3 = "grey"

        elif(self.counter == 100) :
            self.color1 = "grey"
            self.color2 = "grey"
            self.color3 = "black"

        elif(self.counter == 150) : 
            canvas.data["currentScreen"] = canvas.data["nextScreen"]
            canvas.data["nextScreen"] = Screens.SCRN_NONE
            self.reset(canvas)


    def setScreen(self, canvas) : 
        # constants
        X_CENTER = self.X_CENTER
        X_1_THIRD = self.X_1_THIRD
        X_2_THIRD = self.X_2_THIRD
        Y_CENTER = self.Y_CENTER
        Y_1_THIRD = self.Y_1_THIRD
        Y_2_THIRD = self.Y_2_THIRD
        color1 = self.color1
        color2 = self.color2
        color3 = self.color3

        # print the pause screen text
        self.tLevel = canvas.create_text(X_CENTER, Y_1_THIRD, text = canvas.data["level"].getTextLevel(),
                                        font = ("Courier", canvas.data["XL_TEXT_SIZE"]))

        self.tSub = canvas.create_text(X_CENTER, Y_CENTER, text = "Starting in...",
                                        font = ("Courier", canvas.data["L_TEXT_SIZE"]))

        self.t3 = canvas.create_text(X_1_THIRD, Y_2_THIRD, text = "3",
                                        font = ("Courier", canvas.data["XL_TEXT_SIZE"]), fill = color1)  

        self.t2 = canvas.create_text(X_CENTER, Y_2_THIRD, text = "2", 
                                        font = ("Courier", canvas.data["XL_TEXT_SIZE"]), fill = color2)

        self.t1 = canvas.create_text(X_2_THIRD, Y_2_THIRD, text = "1",
                                        font = ("Courier", canvas.data["XL_TEXT_SIZE"]), fill = color3)

    ### draw - make the PauseScreen visible
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


