# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# Level.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
import random
from UI.components.ComponentDefs import *
from UI.components.Block import *
from UI.screens.ScreenEnum import *
import queue

### LEVEL class
class Level :
    ### __init__ - initialize and return Level
    def __init__(self) :
        # constant fields
        self.MAX_LEVELS = 3;

        # dynamic fields
        self.levels = []
        self.currentLevel = 0;
        self.first = True
        self.updated = False

        # level01 - horizontal blocks
        level01 = []
        for x in range(1, 4) :
           for y in range(Y_THIRD, Y_2THIRD, BLOCK_HEIGHT*4) :
                level01.append(Block(x*X_THIRD, y, PowerUps.PWR_NONE, Tilt.HORZ))
        self.levels.append(level01);
        self.blocks = self.levels[0];

        # level02 - vertical blocks
        level02 = []
        for x in range(X_THIRD, X_2THIRD, BLOCK_HEIGHT*4) :
           for y in range(1, 4) :
                level02.append(Block(x, y*Y_THIRD, PowerUps.PWR_NONE, Tilt.VERT)) 
        self.levels.append(level02);       

        # level03 - random horizontal and vertical blocks
        level03 = []
        for x in range(1, 4) :
           for y in range(Y_THIRD, Y_2THIRD, BLOCK_HEIGHT*4) :
                if random.randint(0, 1) == 1 :
                    level03.append(Block(x*X_THIRD, y, PowerUps.PWR_NONE, Tilt.HORZ))
        for x in range(X_THIRD, X_2THIRD, BLOCK_HEIGHT*4) :
           for y in range(1, 4) :
                if random.randint(0, 1) == 1 :
                    level03.append(Block(x, y*Y_THIRD, PowerUps.PWR_NONE, Tilt.VERT)) 
        self.levels.append(level03)

    ### getTextLevel -- get a text version of the current level
    def getTextLevel(self) :
        return 'LEVEL ' + str(self.currentLevel + 1) + '.'

    ### setBlocks -- draw blocks on canvas
    def setBlocks(self, canvas) :
        for block in self.blocks :
            block.ID = block.draw(canvas)

    ### draw -- manage the drawing of the level
    def draw(self, canvas) :
        # complete flag - gets set to 'False' if the level is not completet
        complete = True;

        # if the level has been updated -> redraw the blocks
        if not(self.first) and self.updated :
            for block in self.blocks :
                if(block.enabled == True):
                    complete = False;
                canvas.delete(block.ID)
            self.setBlocks(canvas)
            self.updated = False
            return complete;

        # if this is the first time the level is being draw -> initialize
        elif self.first :
            self.setBlocks(canvas)
            self.first = False 
            return False;

    ### update -- manages the updating of the level and the advancement to the next level
    def update(self, canvas) :
        # levelComplete: True if the level is complete, False otherwise
        levelComplete = self.draw(canvas);

        # current level complete and there is at least one more level to be played
        if levelComplete and ((self.currentLevel + 1) < self.MAX_LEVELS):
            self.currentLevel += 1;
            self.blocks = self.levels[self.currentLevel];
            self.first = True;
            canvas.data['currentScreen'] = Screens.SCRN_PAUSE
            canvas.data['nextScreen'] = Screens.SCRN_GAME
            canvas.data['ball'].reset()

        # current level is complete and there are no more levels to be played ... Game over!
        elif levelComplete and ((self.currentLevel + 1) == self.MAX_LEVELS):
            canvas.data['currentScreen'] = Screens.SCRN_GAME_OVER;


