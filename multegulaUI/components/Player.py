class Player:
    def __init__(self, canvas_width, canvas_height, orientation, state):
        self.paddle = Paddle(canvas_width, canvas_height, orientation, state);
        self.score = 0;
        self.lives = 5;
        self.power = PowerUps.PWR_NONE;