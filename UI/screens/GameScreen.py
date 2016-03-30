# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# GameScreen.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# GameScreen - the paddles, ball, bricks, an status info will be superimposed on this
#   screen during gameplay.
class GameScreen:
    ### __init__ - initialize and return a GameScreen
    ##  @param canvas_width
    ##  @param canvas_height
    def __init__(self, canvas_width, canvas_height):
        self.CANVAS_WIDTH = canvas_width;
        self.CANVAS_HEIGHT = canvas_height;
        self.X_MARGIN = canvas_width // 30;
        self.Y_MARGIN = canvas_height // 30;
        self.first = True;

    def setBackground(self, canvas):
        CANVAS_HEIGHT = self.CANVAS_HEIGHT;
        CANVAS_WIDTH = self.CANVAS_WIDTH;
        X_MARGIN = self.X_MARGIN;
        Y_MARGIN = self.Y_MARGIN;

        self.background = canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill = "black", width = 0);
        self.foreground = canvas.create_rectangle(X_MARGIN, Y_MARGIN, CANVAS_WIDTH - X_MARGIN,
                                                    CANVAS_HEIGHT - Y_MARGIN, fill = "white", width = 0);
    ### drawBackground - draw white background with a white border
    def drawBackground(self, canvas):
        if(self.first):
            self.setBackground(canvas);
            self.first = False;

