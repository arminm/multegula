
class GameScreen:
    def __init__(self, canvas_width, canvas_height):
        self.CANVAS_WIDTH = canvas_width;
        self.CANVAS_HEIGHT = canvas_height;
        self.X_MARGIN = canvas_width // 30;
        self.Y_MARGIN = canvas_height // 30;

    def drawBackground(self, canvas):
        CANVAS_HEIGHT = self.CANVAS_HEIGHT;
        CANVAS_WIDTH = self.CANVAS_WIDTH;
        X_MARGIN = self.X_MARGIN;
        Y_MARGIN = self.Y_MARGIN;

        canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill = "black", width = 0);
        canvas.create_rectangle(X_MARGIN, Y_MARGIN, CANVAS_WIDTH - X_MARGIN,
                                CANVAS_HEIGHT - Y_MARGIN, fill = "white", width = 0);
