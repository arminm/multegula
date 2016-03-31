

class TextField :
    def __init__(self, xCenter, yCenter, initText, textSize) :
        self.X_CENTER = xCenter
        self.Y_CENTER = yCenter
        self.INIT_TEXT = initText
        self.TEXT_SIZE = textSize
        self.text = ""
        self.color = "grey"
        self.first = True
        self.changed = False

    def addChar(self, char) :
        if(self.changed == False) :
            self.text += char
            self.color = "black"
            self.changed = True
        elif(len(self.text) < 16) :
            self.text += char

    def deleteChar(self) :
        self.text = self.text[ :-1]

    def setText(self, canvas) :
        if(self.changed == False) :
            text = self.INIT_TEXT
        else :
            text = self.text

        self.t = canvas.create_text(self.X_CENTER, self.Y_CENTER, 
                                    text = text, 
                                    font = ("Courier", self.TEXT_SIZE), fill = self.color)        
    def draw(self, canvas) :
        if(not(self.first)) :
            canvas.delete(self.t)
            self.setText(canvas)
        else :
            self.setText(canvas)
            self.first = False
