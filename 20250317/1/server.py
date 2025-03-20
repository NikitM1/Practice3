import cmd
import cowsay
import readline
import shlex
import socket

JGSBAT=cowsay.read_dot_cow(open('jgsbat.cow'))
NAMES_LIST=cowsay.list_cows()+['jgsbat']
SIZE=10
WEAPON=['sword','spear','axe']

class Player:
    def __init__(self):
        self.x=self.y=0
    
    def moveHorizontally(self,flag):
        self.x=(self.x+flag)%SIZE
    
    def moveVertically(self,flag):
        self.y=(self.y+flag)%SIZE
    
    def printPosition(self):
        if (self.x, self.y) in game.monsters:
            return 'Moved to '+str((self.x, self.y)),*game.encounter(self.x,self.y)
        return 'Moved to '+str((self.x, self.y))
        
                    

class Monster:
    def __init__(self,name,hitpoints,x,y,speech):
        self.name=name
        if hitpoints<=0: raise ValueError
        self.hitpoints=hitpoints
        if not (0<=x<SIZE and 0<=y<SIZE): raise ValueError
        self.x=x
        self.y=y
        self.speech=speech
    
    def attacked(self,damage):
        damage=min(damage,self.hitpoints)
        self.hitpoints-=damage
        return self.name,self.hitpoints,damage

class MUD:
    def __init__(self):
        self.monsters={}
        self.player=Player()
    
    def move(self,x,y):
        if x:
            self.player.moveHorizontally(x)
        elif y:
            self.player.moveVertically(y)
        return self.player.printPosition()
    
    def encounter(self,x,y):
        return self.monsters[(x,y)].name,self.monsters[(x,y)].speech
    
    def addmon(self,args):
        try:
            if len(args)!=8 or any(p not in args for p in ('hello','hp','coords')):
                raise ValueError
            name=args[0]
            if name not in NAMES_LIST:
                return 'Cannot add unknown monster'
            speech=args[args.index('hello')+1]
            hitpoints=int(args[args.index('hp')+1])
            coords=args.index('coords')
            x,y=int(args[coords+1]),int(args[coords+2]) #if not int then raise ValueError
            f=(x,y) in self.monsters
            self.monsters[(x,y)]=Monster(name,hitpoints,x,y,speech)
            return 'Added monster '+name+' to '+str((x,y))+' saying '+speech+(f*'\nReplaced the old monster')
        except ValueError: return 'Invalid arguments'
    
    def attack(self,args):
        args=shlex.split(args)
        if len(args) not in (1,3) or 'with' in args and args.index('with')!=1:
            return 'Invalid arguments'
        if len(args)==3:
            if (weapon:=args[2]) not in WEAPON:
                return'Unknown weapon'
        else: weapon='sword'
        if (self.player.x,self.player.y) not in self.monsters or self.monsters[(self.player.x,self.player.y)].name!=args[0]:
            return 'No '+args[0]+' here'        
        name,hitpoints,damage=self.monsters[(self.player.x,self.player.y)].attacked(10+WEAPON.index(weapon)*5)
        if hitpoints==0:
            del self.monsters[(self.player.x,self.player.y)]
        return 'Attacked '+name+', damage '+str(damage)+' hp\n'+self.name+(' now has '+str(self.hitpoints) if self.hitpoints else ' died')

def serve(conn,addr):
    print(f'Connected via {addr[0]}:{addr[1]}')
    with conn:
        game=MUD()
        while data:=conn.recv(1024).decode():
            cmd, *args=shlex.split(data)
            match cmd:
                case 'move':
                    response=game.move(args)
                    conn.sendall(shlex.join(response).encode())
                case 'addmon':
                    response=game.addmon(args)
                    conn.sendall(shlex.join(response).encode())
                case 'attack':
                    response=game.attack(args)
                    conn.sendall(shlex.join(response).encode())
    print(f"Disconnected from {addr[0]}:{addr[1]}")

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockfd:
    sockfd.bind((host, port))
    sockfd.listen()
    serve(*sockfd.accept())