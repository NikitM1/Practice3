import cowsay

class Player:
    def __init__(self):
        self.x=self.y=0
    
    def moveHorizontally(self, flag):
        self.x=(self.x+flag)%10
    
    def moveVertically(self, flag):
        self.y=(self.y+flag)%10

class Monster:
    def __init__(self, x, y, speech):
        self.x=x
        self.y=y
        self.speech=speech
    
    def say(self):
        print(cowsay.cowsay(self.speech))

class MUD:
    def __init__(self):
        pass
        