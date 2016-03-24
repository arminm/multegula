from screens.Screens import *

class PausedScreen:
    def __init__(self, canvas_width, canvas_height):
        self.CANVAS_WIDTH = canvas_width;
        self.CANVAS_HEIGHT = canvas_height;
        self.X_CENTER  = canvas_width // 2;
        self.X_1_THIRD = canvas_width * 0.33;
        self.X_2_THIRD = canvas_width * 0.66;
        self.Y_CENTER  = canvas_height // 2;
        self.Y_1_THIRD = canvas_height * 0.33;
        self.Y_2_THIRD = canvas_height * 0.66;
        self.counter = 0;

    def draw(self, canvas):
        X_CENTER = self.X_CENTER;
        X_1_THIRD = self.X_1_THIRD;
        X_2_THIRD = self.X_2_THIRD;
        Y_CENTER = self.Y_CENTER;
        Y_1_THIRD = self.Y_1_THIRD;
        Y_2_THIRD = self.Y_2_THIRD;

        self.counter += 1;
        if(self.counter < 100):
            COLOR1 = "black";
            COLOR2 = "grey";
            COLOR3 = "grey";
        elif(self.counter < 200):
            COLOR1 = "grey";
            COLOR2 = "black";
            COLOR3 = "grey";
        elif(self.counter < 300):
            COLOR1 = "grey";
            COLOR2 = "grey";
            COLOR3 = "black";
        else: 
            canvas.data["currentScreen"] = canvas.data["nextScreen"];
            canvas.data["nextScreen"] = Screens.SCRN_NONE;
            self.counter = 0;
            COLOR1 = "grey";
            COLOR2 = "grey";
            COLOR3 = "grey";

        # print the level
        canvas.create_text(X_CENTER, Y_1_THIRD, text = canvas.data["currentTextLevel"],
                            font = ("Courier", canvas.data["XL_TEXT_SIZE"]));

        canvas.create_text(X_CENTER, Y_CENTER, text = "Starting in...",
                            font = ("Courier", canvas.data["L_TEXT_SIZE"]));

        canvas.create_text(X_1_THIRD, Y_2_THIRD, text = "3",
                            font = ("Courier", canvas.data["XL_TEXT_SIZE"]), fill = COLOR1);  

        canvas.create_text(X_CENTER, Y_2_THIRD, text = "2", 
                            font = ("Courier", canvas.data["XL_TEXT_SIZE"]), fill = COLOR2);

        canvas.create_text(X_2_THIRD, Y_2_THIRD, text = "1",
                            font = ("Courier", canvas.data["XL_TEXT_SIZE"]), fill = COLOR3);


