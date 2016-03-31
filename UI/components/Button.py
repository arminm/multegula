# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# Button.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
class Button :
    ### __init__ - initialize and return button
    ##  canvas_width
    ##  canvas_height
    ##  xCenter - x-coordinate for the center of the button
    ##  yButton - y-coordinate for the center of the button
    ##  text - button label
    ##  active - flag setting the button to be enabled/disabled
    def __init__(self, canvas_width, canvas_height, xCenter, yCenter, text, active) :
        # constant fields
        self.CANVAS_WIDTH = canvas_width
        self.CANVAS_HEIGHT = canvas_height
        self.BUTTON_X_SIZE = canvas_width // 10
        self.BUTTON_Y_SIZE = canvas_height // 20
        self.BUTTON_MARGIN = (canvas_width // 10) - (canvas_width // 11)

        # dynamic fields
        self.xCenter = xCenter
        self.yCenter = yCenter
        self.text = text
        if active == True :
            self.color = "white"
            self.active = True
        else :
            self.color = "grey"
            self.active = False
        self.first = True
    ### get/set location methods
    def setLocation(self, xCenter, yCenter) :
        self.xCenter = xCenter
        self.yCenter = yCenter

    def getLocation(self) :
        return (self.xCenter, self.yCenter)

    ### set/get activity methods
    def makeActive(self) :
        self.color = "white"
        self.active = True

    def makeInactive(self) :
        self.color = "grey"
        self.active = False

    def setButton(self, canvas) :
         # get constants
        BUTTON_X_SIZE = self.BUTTON_X_SIZE
        BUTTON_Y_SIZE = self.BUTTON_Y_SIZE
        BUTTON_MARGIN = self.BUTTON_MARGIN

        # get get button variables
        xCenter = self.xCenter
        yCenter = self.yCenter
        color = self.color
        label = self.text

        # create outter rectangle
        self.background = canvas.create_rectangle(xCenter - BUTTON_X_SIZE, 
                                                    yCenter - BUTTON_Y_SIZE,
                                                    xCenter + BUTTON_X_SIZE,
                                                    yCenter + BUTTON_Y_SIZE, 
                                                    fill = "black")

        # create button's clickable region
        self.foreground = canvas.create_rectangle(xCenter - BUTTON_X_SIZE + BUTTON_MARGIN,
                                                    yCenter - BUTTON_Y_SIZE + BUTTON_MARGIN,
                                                    xCenter + BUTTON_X_SIZE - BUTTON_MARGIN,
                                                    yCenter + BUTTON_Y_SIZE - BUTTON_MARGIN,
                                                    fill = color)

        # set button text
        self.t = canvas.create_text(xCenter, yCenter, text = label,
                                    font = ("Courier", canvas.data["S_TEXT_SIZE"]))  
               
    ### draw - draw the button
    def draw(self, canvas) :
        if not(self.first) :
            canvas.delete(self.background)
            canvas.delete(self.foreground)
            canvas.delete(self.t)
            self.setButton(canvas)
        else :
            self.setButton(canvas)
            self.first = False


    ### clicked - determine if the button has been clicked
    def clicked(self, xClick, yClick) :
        # get constants
        BUTTON_X_SIZE = self.BUTTON_X_SIZE
        BUTTON_Y_SIZE = self.BUTTON_Y_SIZE
        BUTTON_MARGIN = self.BUTTON_MARGIN

        # get button variables
        active = self.active
        xCenter = self.xCenter
        yCenter = self.yCenter

        # return True/False
        if ((active == True) and
            ((xCenter - BUTTON_X_SIZE + BUTTON_MARGIN) < xClick < (xCenter + BUTTON_X_SIZE - BUTTON_MARGIN)) and
            ((yCenter - BUTTON_Y_SIZE + BUTTON_MARGIN) < yClick < (yCenter + BUTTON_Y_SIZE - BUTTON_MARGIN))) :  
            return True
        else : 
            return False

