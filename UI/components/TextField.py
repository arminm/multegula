# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# TextField.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# TEXTFIELD class
class TextField :
    ### __init__ - initialize and return a TextField
    ##  @param xCenter - the x coordinate of the center of this text box
    ##  @param yCenter - the y coordinate of the center of this text box
    ##  @param initText - the intial text of this text field
    ##  @param textSize - the text size of the text in this text field
    def __init__(self, xCenter, yCenter, initText, textSize) :
        self.X_CENTER = xCenter
        self.Y_CENTER = yCenter
        self.INIT_TEXT = initText
        self.TEXT_SIZE = textSize
        self.text = ""
        self.color = "grey"
        self.first = True
        self.changed = False

    ### addChar - add a character to the text field
    def addChar(self, char) :
        if(self.changed == False) :
            self.text += char
            self.color = "black"
            self.changed = True
        elif(len(self.text) < 16) :
            self.text += char

    ### deleteChar - remove the last character from the text field
    def deleteChar(self) :
        self.text = self.text[ :-1]

    ### setText - set the textField in the canvas
    def setText(self, canvas) :
        if(self.changed == False) :
            text = self.INIT_TEXT
        else :
            text = self.text

        self.t = canvas.create_text(self.X_CENTER, self.Y_CENTER, 
                                    text = text, 
                                    font = ("Courier", self.TEXT_SIZE), fill = self.color) 
        
    ### draw - manages the drawing of the text field       
    def draw(self, canvas) :
        if(not(self.first)) :
            canvas.delete(self.t)
            self.setText(canvas)
        else :
            self.setText(canvas)
            self.first = False
