
from components.DirectionEnum import *

class Paddle:
    def __init__(self, canvas_width, canvas_height, orientation):
        self.CANVAS_WIDTH = canvas_width;
        self.CANVAS_HEIGHT = canvas_height;
        self.MARGIN = canvas_width // 30;
        self.PADDLE_MARGIN = canvas_height // 20;
        self.PADDLE_HEIGHT = canvas_height // 50;   
        self.MIN = self.MARGIN + self.PADDLE_HEIGHT;
        self.MAX = canvas_width - self.MARGIN   - self.PADDLE_HEIGHT;   
        self.BORDER_WIDTH = canvas_width // 350;
        self.ORIENTATION = orientation;
        self.width = canvas_width // 6;
        self.center = canvas_width // 2;
        self.speed = canvas_width // 70; 

        self.COLORS = ["red", "green", "blue", "purple", "orange", "yellow", "black", "white"];
        self.color = "black";

    def randomColor(self):
        currentColor = self.color;
        newColor = currentColor;

        # loop until a new color has been chosen
        while (currentColor == newColor):
            newColor = random.choice(self.COLORS);

        # set new color
        self.color = newColor;

    def getColor(self):
        return self.color;

    def move(self, direction):
        MIN = self.MIN;
        MAX = self.MAX;

        if(direction == Direction.DIR_LEFT):
            if((self.center - self.width) > self.MIN):
                self.center = self.center - self.speed;
        elif(direction == Direction.DIR_RIGHT):
            if((self.center + self.width) < self.MAX):
                self.center = self.center + self.speed;

    def draw(self, canvas): 
        CANVAS_HEIGHT = self.CANVAS_HEIGHT;
        PADDLE_MARGIN = self.PADDLE_MARGIN;
        PADDLE_HEIGHT = self.PADDLE_HEIGHT;
        BORDER_WIDTH = self.BORDER_WIDTH; 

        center = self.center;
        width = self.width;
        color = self.color;

        if(self.orientation == Orientation.DIR_NORTH):
            # draw paddle at the top of the screen
            canvas.create_rectangle(center - width, 
                                    PADDLE_MARGIN,
                                    center + width,
                                    PADDLE_MARGIN + PADDLE_HEIGHT,
                                    fill = color, width = BORDER_WIDTH)
        # draw paddle at the bottom of the screen
        elif(self.orientation == Orientation.DIR_SOUTH):
            canvas.create_rectangle(center - width,
                                    CANVAS_HEIGHT - PADDLE_HEIGHT - PADDLE_MARGIN,
                                    center + width,
                                    CANVAS_HEIGHT - PADDLE_MARGIN,
                                    fill = color, width = BORDER_WIDTH);
        elif(self.orientation == Orientation.EAST):
            # draw paddle on the right
            canvas.create_rectangle(CANVAS_WIDTH - PADDLE_MARGIN - PADDLE_HEIGHT,
                                    CANVAS_WIDTH - PADDLE_MARGIN,
                                    center + width,
                                    fill = color, width = borderWidth)
        # draw paddle on the left
        elif(self.orientation == Orientation.WEST):
            canvas.create_rectangle(PADDLE_MARGIN,
                                    center - width,
                                    PADDLE_MARGIN + PADDLE_HEIGHT,
                                    center + width,
                                    fill = color, width = BORDER_WIDTH)




