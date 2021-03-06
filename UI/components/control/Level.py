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
        self.MAX_LEVELS = len(glob.glob('UI/levels/*.py',recursive=True));

        # dynamic fields
        self.levels = []
        self.currentLevel = 0;
        self.first = True
        self.updated = False
        self.levelOrientation = Orientation.DIR_SOUTH;

        # Read all level files
        for level in sorted(glob.glob('UI/levels/*.py',recursive=True)):
        	self.readLevel(level)
    
        # set first level
        self.blocks = self.levels[0]

    ### readLevel - parse level as defined in py level file
    def readLevel(self, levelpath) :
        # make a blank level
        thisLevel = []
        
        #Execfile is gone in Python 3, need to do it this way for now
        exec(open(levelpath).read())
        # makeBlock parses the line and makes a new block
        self.levels.append(thisLevel)

    ### getTextLevel -- get a text version of the current level
    def getTextLevel(self) :
        return 'LEVEL ' + str(self.currentLevel + 1) + '.'

    ### setBlocks -- draw blocks on canvas
    def setBlocks(self, canvas) :
        for block in self.blocks :
            block.ID = block.draw(canvas, self.levelOrientation)

    ### isComplete - determine if the level is complete
    def isComplete(self) :
        for block in self.blocks :
            if block.enabled == True:
                return False

        return True

    ### draw -- manage the drawing of the level
    def draw(self, canvas) :
        # if the level has been updated -> redraw the blocks
        if not(self.first) and self.updated :
            self.setBlocks(canvas)
            self.updated = False

        # if this is the first time the level is being draw -> initialize
        elif self.first :
            self.setBlocks(canvas)
            self.first = False 

    ### update -- manages the updating of the level and the advancement to the next level
    def update(self, canvas) :
        # levelComplete: True if the level is complete, False otherwise
        levelComplete = self.isComplete()
        self.draw(canvas)

        # current level complete and there is at least one more level to be played
        if levelComplete and (self.currentLevel + 1) < self.MAX_LEVELS :
            self.currentLevel += 1;
            self.blocks = self.levels[self.currentLevel];
            self.first = True;
            return LevelReturnStatus.COMPLETE

        # current level is complete and there are no more levels to be played ... Game over!
        elif levelComplete and (self.currentLevel + 1) == self.MAX_LEVELS:
            return LevelReturnStatus.GAME_OVER

        # nothing significant
        else : 
            return LevelReturnStatus.NO_STATUS

