from components.ComponentDefs import *
from components.Block import *
import queue

class Level :
    def __init__(self, canvas_width, canvas_height) :
        self.CANVAS_WIDTH = canvas_width
        self.CANVAS_HEIGHT = canvas_height

        self.blocks = []
        self.enabled = []
        self.updateQueue = queue.Queue()

        BLOCK_WIDTH = canvas_width // 10
        BLOCK_HEIGHT = canvas_height // 25  

        X_THIRD     = (canvas_width // 4)
        Y_START     = (canvas_height // 4) 
        Y_END       = (canvas_height // 4)*3

        for x in range(1, 4) :
           for y in range(Y_START, Y_END, BLOCK_HEIGHT*2) :
                self.blocks.append(Block(canvas_width, canvas_height, x*X_THIRD, y, PowerUps.PWR_NONE, Tilt.HORZ))

        self.first = True
        self.updated = False


    def setBlocks(self, canvas) :
        for block in self.blocks :
            block.ID = block.draw(canvas)

    def draw(self, canvas) :
        if not(self.first) and self.updated :
            for block in self.blocks :
                canvas.delete(block.ID)
            self.setBlocks(canvas)
            self.updated = False
        elif self.first :
            self.setBlocks(canvas)
            self.first = False

    def breakBlock(self, canvas) :
        (ballLeft, ballRight, ballTop, ballBottom) = canvas.data["ball"].getEdges()
        (ballCenterX, ballCenterY, ballRadius) = canvas.data["ball"].getInfo()
        (xVelocity, yVelocity) = canvas.data["ball"].getVelocity()


        # ball moving NORTH WEST
        if(xVelocity < 0) and (yVelocity <= 0) :
            for i, block in enumerate(self.blocks) :
                if(block.enabled == True) :
                    (blkLeft, blkRight, blkTop, blkBottom) = block.getEdges()
                    if (ballTop <= blkBottom) and (ballBottom > blkBottom) and (blkLeft <= ballCenterX <= blkRight) :
                        canvas.data["ball"].setVelocity(xVelocity, (-yVelocity))
                        self.blocks[i].disable()
                        self.updated = True
                    elif (ballLeft <= blkRight) and (ballRight > blkRight) and (blkTop <= ballCenterY <= blkBottom) :
                        canvas.data["ball"].setVelocity((-xVelocity), yVelocity)
                        self.blocks[i].disable()
                        self.updated = True                                       

        # ball moving NORTH EAST
        elif(xVelocity > 0) and (yVelocity < 0) :
            for i, block in enumerate(self.blocks) :
                if(block.enabled == True) :
                    (blkLeft, blkRight, blkTop, blkBottom) = block.getEdges()
                    if (ballTop <= blkBottom) and (ballBottom > blkBottom) and (blkLeft <= ballCenterX <= blkRight) :
                        canvas.data["ball"].setVelocity(xVelocity, (-yVelocity))
                        self.blocks[i].disable()
                        self.updated = True
                    elif (ballRight >= blkLeft) and (ballLeft < blkRight) and (blkTop <= ballCenterY <= blkBottom) :
                        canvas.data["ball"].setVelocity((-xVelocity), yVelocity)
                        self.blocks[i].disable()
                        self.updated = True                                          
          
        # ball moving SOUTH WEST
        elif(xVelocity < 0) and (yVelocity > 0) :
            for i, block in enumerate(self.blocks) :
                if(block.enabled == True) :
                    (blkLeft, blkRight, blkTop, blkBottom) = block.getEdges()
                    if (ballBottom >= blkTop) and (ballTop < blkTop) and (blkLeft <= ballCenterX <= blkRight) :
                        canvas.data["ball"].setVelocity(xVelocity, (-yVelocity))
                        self.blocks[i].disable()
                        self.updated = True
                    elif (ballLeft <= blkRight) and (ballRight > blkRight) and (blkTop <= ballCenterY <= blkBottom) :
                        canvas.data["ball"].setVelocity((-xVelocity), yVelocity)
                        self.blocks[i].disable()
                        self.updated = True  

        # ball moving SOUTH EAST
        elif(xVelocity > 0) and (yVelocity > 0) :
            for i, block in enumerate(self.blocks) :
                if(block.enabled == True) :
                    (blkLeft, blkRight, blkTop, blkBottom) = block.getEdges()
                    if (ballBottom >= blkTop) and (ballTop < blkTop) and (blkLeft <= ballCenterX <= blkRight) :
                        canvas.data["ball"].setVelocity(xVelocity, (-yVelocity))
                        self.blocks[i].disable()
                        self.updated = True
                    elif (ballRight >= blkLeft) and (ballLeft < blkRight) and (blkTop <= ballCenterY <= blkBottom) :
                        canvas.data["ball"].setVelocity((-xVelocity), yVelocity)
                        self.blocks[i].disable()
                        self.updated = True     

    def update(self, canvas) :
        if not(self.first) :
            self.breakBlock(canvas)
            self.draw(canvas)
        else :
            self.draw(canvas)

