from components.ComponentDefs import *
from components.Block import *
from screens.ScreenEnum import *
import queue

class Level :
    def __init__(self, canvas_width, canvas_height) :
        self.CANVAS_WIDTH = canvas_width
        self.CANVAS_HEIGHT = canvas_height

        self.levels = []
        self.MAX_LEVELS = 2;
        self.currentLevel = 0;

        BLOCK_WIDTH = canvas_width // 10
        BLOCK_HEIGHT = canvas_height // 25  

        X_THIRD     = canvas_width // 4
        X_START     = X_THIRD
        X_END       = X_THIRD*3
        Y_THIRD     = canvas_height // 4
        Y_START     = Y_THIRD 
        Y_END       = Y_THIRD*3

        level01 = [];
        for x in range(1, 4) :
           for y in range(Y_START, Y_END, BLOCK_HEIGHT*2) :
                level01.append(Block(canvas_width, canvas_height, x*X_THIRD, y, PowerUps.PWR_NONE, Tilt.HORZ))
        self.levels.append(level01);

        level02 = [];
        for x in range(X_START, X_END, BLOCK_HEIGHT*2) :
           for y in range(1, 4) :
                level02.append(Block(canvas_width, canvas_height, x, y*Y_THIRD, PowerUps.PWR_NONE, Tilt.VERT)) 

        self.levels.append(level02);       

        self.blocks = self.levels[0];
        self.first = True
        self.updated = False

    def getTextLevel(self):
        return "LEVEL " + str(self.currentLevel + 1) + "."

    def setBlocks(self, canvas) :
        for block in self.blocks :
            block.ID = block.draw(canvas)

    def draw(self, canvas) :
        incomplete = False;
        if not(self.first) and self.updated :
            for block in self.blocks :
                if(block.enabled == True):
                    incomplete = True;
                canvas.delete(block.ID)
            self.setBlocks(canvas)
            self.updated = False
            return incomplete;
        elif self.first :
            self.setBlocks(canvas)
            self.first = False 
            return True;


    def update(self, canvas) :
        levelIncomplete = self.draw(canvas);
        if(levelIncomplete == False) and ((self.currentLevel + 1) < self.MAX_LEVELS):
            self.currentLevel += 1;
            self.blocks = self.levels[self.currentLevel];
            self.first = True;
            canvas.data["currentScreen"] = Screens.SCRN_PAUSE
            canvas.data["nextScreen"] = Screens.SCRN_GAME
            canvas.data["ball"].reset()
        elif (levelIncomplete == False) and ((self.currentLevel + 1) == self.MAX_LEVELS):
            canvas.data["currentScreen"] = Screens.SCRN_GAME_OVER;


