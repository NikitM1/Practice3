import cmd
import cowsay
import readline
import shlex

JGSBAT=cowsay.read_dot_cow(open('jgsbat.cow'))
SIZE=10
WEAPON=['sword','spear','axe']

class Player:
    def __init__(self):
        self.x=self.y=0
    
    def moveHorizontally(self,flag):
        self.x=(self.x+flag)%SIZE
        self.printPosition()
    
    def moveVertically(self,flag):
        self.y=(self.y+flag)%SIZE
        self.printPosition()
    
    def printPosition(self):
        print('Moved to', (self.x, self.y))
        if (self.x, self.y) in game.monsters:
            game.encounter(self.x,self.y)        

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
    
    def attacked(self,damage):
        damage=min(damage,self.hitpoints)
        self.hitpoints-=damage
        print('Attacked '+self.name+', damage',damage,'hp')
        print(self.name+(' now has '+str(self.hitpoints) if self.hitpoints else ' died'))
        return self.hitpoints

class MUD(cmd.Cmd):
    intro='<<< Welcome to Python-MUD 0.1 >>>'
    prompt='>>>'
    
    def encounter(self,x,y):
        self.monsters[(x,y)].say()
    
    def do_up(self,args):
        if args: print('Invalid arguments')
        else: player.moveVertically(-1)
    
    def do_down(self,args):
        if args: print('Invalid arguments')
        else: player.moveVertically(1)
    
    def do_left(self,args):
        if args: print('Invalid arguments')
        else: player.moveHorizontally(-1)
    
    def do_right(self,args):
        if args: print('Invalid arguments')
        else: player.moveHorizontally(1)
    
    def do_addmon(self,args):
        c=shlex.split(args)
        try:
            if len(c)!=8 or any(p not in c for p in ('hello','hp','coords')):
                raise ValueError
            name=c[0]
            if name not in cowsay.list_cows()+['jgsbat']:
                print('Cannot add unknown monster')
                return
            speech=c[c.index('hello')+1]
            hitpoints=int(c[c.index('hp')+1])
            coords=c.index('coords')
            x,y=int(c[coords+1]),int(c[coords+2]) #if not int then raise ValueError
            f=(x,y) in self.monsters
            self.monsters[(x,y)]=Monster(name,hitpoints,x,y,speech)
            print('Added monster', name, 'to', (x,y), 'saying', speech)
            if f: print('Replaced the old monster')
        except ValueError: print('Invalid arguments')  
    
    def do_attack(self,args):
        args=shlex.split(args)
        if len(args)==1 or len(args)>2 or 'with' in args and args.index('with')!=0:
            print('Invalid arguments')
            return
        if args:
            if (weapon:=args[1]) not in WEAPON:
                print('Unknown weapon')
                return
        else: weapon='sword'
        if (player.x,player.y) not in self.monsters:
            print('No monster here')
            return
        if self.monsters[(player.x,player.y)].attacked(10+WEAPON.index(weapon)*5)==0:
            del self.monsters[(player.x,player.y)]
    
    def complete_attack(self, text, line, begidx, endidx):
         args=shlex.split(line[:begidx],False,False)
         if args[-1]=='with':
             return [c for c in WEAPON if c.startswith(text)]
    
    def do_EOF(self,args):
        return 1
    
    def do_default(self):
        print('Invalid command')

if __name__=='__main__':
    player=Player()
    game=MUD()
    game.monsters={}
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")    
    game.cmdloop()