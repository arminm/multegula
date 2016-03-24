class Button:
    def __init__(self, canvas_width, canvas_height, xCenter, yCenter, text, active):
        self.CANVAS_WIDTH = canvas_width;
        self.CANVAS_HEIGHT = canvas_height;
        self.BUTTON_X_SIZE = canvas_width // 10;
        self.BUTTON_Y_SIZE = canvas_height // 20;
        self.BUTTON_MARGIN = (canvas_width // 10) - (canvas_width // 11)
        self.xCenter = xCenter;
        self.yCenter = yCenter;
        self.text = text;
        if(active == True):
            self.color = "white";
            self.active = True;
        else:
            self.color = "grey";
            self.active = False;

    # get/set location methods
    def setLocation(self, xCenter, yCenter):
        self.xCenter = xCenter;
        self.yCenter = yCenter;

    def getLocation(self):
        return (self.xCenter, self.yCenter);

    # set/get activity methods
    def makeActive(self):
        self.color = "white"
        self.active = True;

    def makeInactive(self):
        self.color = "grey";
        self.active = False;

    def getActive(self):
        return self.active;

    def draw(self, canvas):
        BUTTON_X_SIZE = self.BUTTON_X_SIZE;
        BUTTON_Y_SIZE = self.BUTTON_Y_SIZE;
        BUTTON_MARGIN = self.BUTTON_MARGIN;
        xCenter = self.xCenter;
        yCenter = self.yCenter;
        color = self.color;
        label = self.text;

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
        font = ("Courier", canvas.data["S_TEXT_SIZE"]));   

    def clicked(self, xClick, yClick):
        BUTTON_X_SIZE = self.BUTTON_X_SIZE;
        BUTTON_Y_SIZE = self.BUTTON_Y_SIZE;
        BUTTON_MARGIN = self.BUTTON_MARGIN;

        active = self.active;
        xCenter = self.xCenter;
        yCenter = self.yCenter;


        if ((active == True) and
            ((xCenter - BUTTON_X_SIZE + BUTTON_MARGIN) < xClick < (xCenter + BUTTON_X_SIZE - BUTTON_MARGIN)) and 
            ((yCenter - BUTTON_Y_SIZE + BUTTON_MARGIN) < yClick < (yCenter + BUTTON_Y_SIZE - BUTTON_MARGIN))):  
            return True;
        else: 
            return False;