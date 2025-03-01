import cowsay

SIZE=10

class Player:
    def __init__(self):
        self.x=self.y=0
    
    def moveHorizontally(self,flag):
        self.x=(self.x+flag)%SIZE
    
    def moveVertically(self,flag):
        self.y=(self.y+flag)%SIZE

class Monster:
    def __init__(self,name,x,y,speech):
        self.name=name
        self.x=x
        self.y=y
        self.speech=speech
    
    def say(self):
        print(cowsay.cowsay(self.speech))

class MUD:
    def __init__(self):
        self.monsters={}
    
    def encounter(self,x,y):
        self.monsters[(x,y)].say()
    
    def play(self):
        player=Player()
        while s:=input().strip():
            c=s.split()
            try:
                match t:=(c[0].lower()):
                    case 'up'|'down'|'left'|'right':
                        if len(c)>1: raise ValueError
                        player.moveHorizontally((t=='right')-(t=='left'))
                        player.moveVertically((t=='down')-(t=='up'))
                        print('Moved to', (player.x, player.y))
                        if (player.x, player.y) in self.monsters:
                            self.encounter(player.x,player.y)
                    case 'addmon':
                        try:
                            speech=c[4]
                            for i in range(5,len(c)): speech+=' '+c[i]
                            name=c[1]
                            if name not in cowsay.list_cows():
                                print('Cannot add unknown monster')
                                continue
                            x,y=int(c[2]),int(c[3])
                            f=(x,y) in self.monsters
                            self.monsters[(x,y)]=Monster(name,x,y,speech)
                            print('Added monster', name, 'to', (x,y), 'saying', speech)
                            if f: print('Replaced the old monster')
                        except: raise ValueError
                    case _: raise AttributeError
            except ValueError: print('Invalid arguments')
            except AttributeError: print('Invalid command')
    
MUD().play()