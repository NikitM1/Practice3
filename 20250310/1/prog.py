import cowsay
import shlex

SIZE=10
JGSBAT=cowsay.read_dot_cow(open('jgsbat.cow'))

class Player:
    def __init__(self):
        self.x=self.y=0
    
    def moveHorizontally(self,flag):
        self.x=(self.x+flag)%SIZE
    
    def moveVertically(self,flag):
        self.y=(self.y+flag)%SIZE

class Monster:
    def __init__(self,name,hitpoints,x,y,speech):
        self.name=name
        if hitpoints<=0: raise ValueError
        self.hitpoints=hitpoints
        if not (0<=x<SIZE and 0<=y<SIZE): raise ValueError
        self.x=x
        self.y=y
        self.speech=speech
    
    def say(self):
        if self.name!='jgsbat':
            print(cowsay.cowsay(self.speech,cow=self.name))
        else: print(cowsay.cowsay(self.speech,cowfile=JGSBAT))

class MUD:
    def __init__(self):
        self.monsters={}
    
    def encounter(self,x,y):
        self.monsters[(x,y)].say()
    
    def printGreeting(self):
        print('<<< Welcome to Python-MUD 0.1 >>>')
    
    def play(self):
        player=Player()
        self.printGreeting()
        while s:=input():
            c=shlex.split(s)
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
                        if len(c)!=9 or any(p not in c for p in ('hello','hp','coords')): raise ValueError
                        name=c[1]
                        if name not in cowsay.list_cows()+['jgsbat']:
                            print('Cannot add unknown monster')
                            continue
                        speech=c[c.index('hello')+1]
                        hitpoints=int(c[c.index('hp')+1])
                        coords=c.index('coords')
                        x,y=int(c[coords+1]),int(c[coords+2]) #if not int then raise ValueError
                        f=(x,y) in self.monsters
                        self.monsters[(x,y)]=Monster(name,hitpoints,x,y,speech)
                        print('Added monster', name, 'to', (x,y), 'saying', speech)
                        if f: print('Replaced the old monster')
                    case _: raise AttributeError
            except ValueError: print('Invalid arguments')
            except AttributeError: print('Invalid command')
    
MUD().play()
