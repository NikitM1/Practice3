import cmd
import readline
import shlex
import socket
import sys

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
            return str(self.x),str(self.y),*game.encounter(self.x,self.y)
        return str(self.x),str(self.y)
        
                    

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
        return self.hitpoints,damage

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
    
    def addmon(self,name,hitpoints,x,y,speech):
        f=(x,y) in self.monsters
        self.monsters[(x,y)]=Monster(name,hitpoints,x,y,speech)
        return str(f)
    
    def attack(self,name,damage):
        if (self.player.x,self.player.y) not in self.monsters or self.monsters[(self.player.x,self.player.y)].name!=name:
            return '-1 -1'       
        hitpoints,damage=self.monsters[(self.player.x,self.player.y)].attacked(10+WEAPON.index(weapon)*5)
        if hitpoints==0:
            del self.monsters[(self.player.x,self.player.y)]
        return map(str,[hitpoints,damage])

def serve(conn,addr):
    print(f'Connected via {addr[0]}:{addr[1]}')
    with conn:
        global game
        game=MUD()
        while data:=conn.recv(1024).decode():
            cmd, *args=shlex.split(data)
            match cmd:
                case 'move':
                    response=game.move(*list(map(int,args)))
                    conn.sendall(shlex.join(response).encode())
                case 'addmon':
                    response=game.addmon(args[0],int(args[1]),int(args[2]),int(args[3]),args[4])
                    conn.sendall(shlex.join(response).encode())
                case 'attack':
                    response=game.attack(args[0],int(args[1]))
                    conn.sendall(shlex.join(response).encode())
    print(f'Disconnected from {addr[0]}:{addr[1]}')

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockfd:
    sockfd.bind((host, port))
    sockfd.listen()
    serve(*sockfd.accept())