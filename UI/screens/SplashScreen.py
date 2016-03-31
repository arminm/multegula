# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# SplashScreen.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# SplashScreen - first thing visible to a user. A name prompt is to be superimposed
#   over top of this class.
class SplashScreen :
    ### __init__ - initialize and return a MenuScreen
    ##  @param canvas_width
    ##  @param canvas_height
    def __init__(self, canvas_width, canvas_height) :
        self.CANVAS_WIDTH = canvas_width
        self.CANVAS_HEIGHT = canvas_height
        self.X_MARGIN = canvas_width // 30
        self.Y_MARGIN = canvas_height // 30
        self.X_CENTER = canvas_width // 2
        self.Y_LOC_TITLE = 0.25*canvas_height
        self.Y_LOC_PROMPT = 0.50*canvas_height
        self.firstBack = True
        self.firstText = True


    def setBackground(self, canvas) :
        # constants
        CANVAS_HEIGHT = self.CANVAS_HEIGHT
        CANVAS_WIDTH = self.CANVAS_WIDTH
        X_MARGIN = self.X_MARGIN
        Y_MARGIN = self.Y_MARGIN

        # draw text
        self.background = canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill = "black", width = 0)
        self.foreground = canvas.create_rectangle(X_MARGIN, Y_MARGIN, CANVAS_WIDTH - X_MARGIN,
                                                    CANVAS_HEIGHT - Y_MARGIN, fill = "white", width = 0)  

    def setText(self, canvas) :
        # constants
        Y_LOC_TITLE = self.Y_LOC_TITLE
        Y_LOC_PROMPT = self.Y_LOC_PROMPT
        X_CENTER = self.X_CENTER
        XL_TEXT_SIZE = canvas.data["XL_TEXT_SIZE"]
        M_TEXT_SIZE = canvas.data["M_TEXT_SIZE"]

        # draw text
        self.title = canvas.create_text(X_CENTER, Y_LOC_TITLE, text = "MULTEGULA",
                                        font = ("Courier", XL_TEXT_SIZE))
        self.prompt = canvas.create_text(X_CENTER, Y_LOC_PROMPT, text = "Welcome. Tell us your name...",
                                            font = ("Courier", M_TEXT_SIZE))    

    def drawBackground(self, canvas) :
        if(self.firstBack) :
            self.setBackground(canvas)
            self.firstBack = False

    def drawText(self, canvas) :
        if(not(self.firstText)) :
            canvas.delete(self.title)
            canvas.delete(self.prompt)
            self.setText(canvas)
        else :
            self.setText(canvas)
            self.firstText = False


