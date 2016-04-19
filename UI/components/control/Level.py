# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# Level.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
import queue
import random
import glob
from UI.typedefs import *
from UI.components.gameplay.Block import *

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

        # Read all level files
        for level in glob.glob('UI/levels/*.mlev',recursive=True):
        	self.readLevel(level)
    
        # set first level
        self.blocks = self.levels[0]

    ### readLevel - parse level as defined in mlev file
    def readLevel(self, levelpath) :
        # make a blank level
        thisLevel = []
        #Execfile is gone in Python 3, need to do it this way for now
        exec(open(levelpath).read())
        # makeBlock parses the line and makes a new block
        #thisLevel.append(makeBlock(line))
        self.levels.append(thisLevel)

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
                if block.enabled == True:
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
        if levelComplete and (self.currentLevel + 1) < self.MAX_LEVELS :
            self.currentLevel += 1;
            self.blocks = self.levels[self.currentLevel];
            self.first = True;
            canvas.data['currentScreen'] = Screens.SCRN_PAUSE
            canvas.data['nextScreen'] = Screens.SCRN_GAME
            canvas.data['ball'].reset()

        # current level is complete and there are no more levels to be played ... Game over!
        elif levelComplete and (self.currentLevel + 1) == self.MAX_LEVELS:
            canvas.data['currentScreen'] = Screens.SCRN_GAME_OVER;


