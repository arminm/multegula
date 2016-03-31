class GameOver :
    ### __init__ - initialize and return a GameScreen
    ##  @param canvas_width
    ##  @param canvas_height
    def __init__(self, canvas_width, canvas_height) :
        self.CANVAS_WIDTH = canvas_width
        self.CANVAS_HEIGHT = canvas_height
        self.X_MARGIN = canvas_width // 30
        self.Y_MARGIN = canvas_height // 30
        self.Y_LOC_TITLE = 0.25*canvas_height
        self.X_CENTER = canvas_width // 2
        self.Y_CENTER = canvas_height // 2
        self.first = True

    def setBackground(self, canvas) :
        CANVAS_HEIGHT = self.CANVAS_HEIGHT
        CANVAS_WIDTH = self.CANVAS_WIDTH
        X_MARGIN = self.X_MARGIN
        Y_MARGIN = self.Y_MARGIN
        X_CENTER = self.X_CENTER
        Y_CENTER = self.Y_CENTER;
        Y_LOC_TITLE = self.Y_LOC_TITLE;

        L_TEXT_SIZE = canvas.data["L_TEXT_SIZE"]
        XL_TEXT_SIZE = canvas.data["XL_TEXT_SIZE"]


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