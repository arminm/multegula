from components.ComponentDefs import *

class GameOver :
    ### __init__ - initialize and return a GameScreen
    ##  @param canvas_width
    ##  @param canvas_height
    def __init__(self) :
        self.first = True

    def setBackground(self, canvas) :
        self.background = canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill = "black", width = 0)

        self.foreground = canvas.create_rectangle(X_MARGIN, Y_MARGIN, CANVAS_WIDTH - X_MARGIN,
                                                    CANVAS_HEIGHT - Y_MARGIN, fill = "white", width = 0)

        self.title  = canvas.create_text(X_CENTER, Y_LOC_TITLE, text = "MULTEGULA",
                                        font = ("Courier", XL_TEXT_SIZE))
        
        self.title  = canvas.create_text(X_CENTER, Y_CENTER, text = "GAME OVER.",
                                        font = ("Courier", L_TEXT_SIZE))
    ### drawBackground - draw white background with a white border
    def drawBackground(self, canvas) :
        if(self.first) :
            self.setBackground(canvas)
            self.first = False