
class MenuScreen:
    def __init__(self, canvas_width, canvas_height):
        self.CANVAS_WIDTH = canvas_width;
        self.CANVAS_HEIGHT = canvas_height;
        self.X_MARGIN = canvas_width // 30;
        self.Y_MARGIN = canvas_height // 30;
        self.X_CENTER = canvas_width // 2;
        self.Y_LOC_TITLE = 0.25*canvas_height;
        self.Y_LOC_AUTHOR1 = 0.45*canvas_height;
        self.Y_LOC_AUTHOR2 = 0.50*canvas_height;

    def drawBackground(self, canvas):
        CANVAS_HEIGHT = self.CANVAS_HEIGHT;
        CANVAS_WIDTH = self.CANVAS_WIDTH;
        X_MARGIN = self.X_MARGIN;
        Y_MARGIN = self.Y_MARGIN;

        canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill = "black", width = 0);
        canvas.create_rectangle(X_MARGIN, Y_MARGIN, CANVAS_WIDTH - X_MARGIN,
                                CANVAS_HEIGHT - Y_MARGIN, fill = "white", width = 0);

    def drawText(self, canvas):
        Y_LOC_TITLE = self.Y_LOC_TITLE;
        Y_LOC_AUTHOR1 = self.Y_LOC_AUTHOR1;
        Y_LOC_AUTHOR2 = self.Y_LOC_AUTHOR2;
        X_CENTER = self.X_CENTER;
        XL_TEXT_SIZE = canvas.data["XL_TEXT_SIZE"];
        M_TEXT_SIZE = canvas.data["M_TEXT_SIZE"];

        canvas.create_text(X_CENTER, Y_LOC_TITLE, text = "MULTEGULA",
                            font = ("Courier", XL_TEXT_SIZE));
        canvas.create_text(X_CENTER, Y_LOC_AUTHOR1, text = "created by",
                            font = ("Courier", M_TEXT_SIZE));
        canvas.create_text(X_CENTER, Y_LOC_AUTHOR2, text = "DS Team Misfits",
                            font = ("Courier", M_TEXT_SIZE));
