import cmd
import cowsay
import readline
import shlex
import socket
import sys

JGSBAT=cowsay.read_dot_cow(open('jgsbat.cow'))
NAMES_LIST=cowsay.list_cows()+['jgsbat']
SIZE=10
WEAPON=['sword','spear','axe']

def move(x,y,name='',speech=''):
    print('Moved to ('+x+', '+y+')')
    if name=='jgsbat':
        print(cowsay.cowsay(speech,cowfile=JGSBAT))
    elif name:
        print(cowsay.cowsay(speech,cow=name))

def addmon(name,x,y,speech,f):
    print('Added monster', name, 'to', (x,y), 'saying', speech)
    if f: print('Replaced the old monster')

def attack(name,hitpoints,damage):
    if damage=='-1':
        print('No',name,'here')
        return
    print('Attacked '+name+', damage',damage,'hp')
    print(name+(' now has '+str(hitpoints) if int(hitpoints) else ' died'))    

class MUD(cmd.Cmd):
    intro='<<< Welcome to Python-MUD 0.1 >>>'
    prompt='>>>'
    
    def __init__(self,socket):
        super().__init__()
        self.socket=socket
    
    def do_up(self,args):
        if args: print('Invalid arguments')
        else: 
            self.socket.sendall(b'move 0 1')
            move(*shlex.split(self.socket.recv(1024).decode()))
    
    def do_down(self,args):
        if args: print('Invalid arguments')
        else: 
            self.socket.sendall(b'move 0 -1')
            move(*shlex.split(self.socket.recv(1024).decode()))            
    
    def do_left(self,args):
        if args: print('Invalid arguments')
        else: 
            self.socket.sendall(b'move -1 0')
            move(*shlex.split(self.socket.recv(1024).decode()))            
    
    def do_right(self,args):
        if args: print('Invalid arguments')
        else: 
            self.socket.sendall(b'move 1 0')
            move(*shlex.split(self.socket.recv(1024).decode()))            
    
    def do_addmon(self,args):
        c=shlex.split(args)
        try:
            if len(c)!=8 or any(p not in c for p in ('hello','hp','coords')):
                raise ValueError
            name=c[0]
            if name not in NAMES_LIST:
                print('Cannot add unknown monster')
                return
            speech=c[c.index('hello')+1]
            hitpoints=int(c[c.index('hp')+1])
            if hitpoints<=0: raise ValueError
            coords=c.index('coords')
            x,y=int(c[coords+1]),int(c[coords+2]) #if not int then raise ValueError
            if not (0<=x<SIZE and 0<=y<SIZE): raise ValueError
            self.socket.sendall(shlex.join(['addmon',name,str(hitpoints),str(x),str(y),speech]).encode())
            addmon(name,x,y,speech,bool(int(self.socket.recv(1024).decode())))
        except ValueError: print('Invalid arguments')
    
    def do_attack(self,args):
        args=shlex.split(args)
        if len(args) not in (1,3) or 'with' in args and args.index('with')!=1:
            print('Invalid arguments')
            return
        if len(args)==3:
            if (weapon:=args[2]) not in WEAPON:
                print('Unknown weapon')
                return
        else: weapon='sword'
        self.socket.sendall(shlex.join(['attack',args[0],str(10+WEAPON.index(weapon)*5)]).encode())
        attack(args[0],*shlex.split(self.socket.recv(1024).decode()))
    
    def complete_attack(self, text, line, begidx, endidx):
        args = shlex.split(line[:begidx], False, False)
        if args[-1] == 'attack':
            return [c for c in NAMES_LIST if c.startswith(text)]
        elif args[-1]=='with':
            return [c for c in WEAPON if c.startswith(text)]
    
    def do_EOF(self,args):
        return 1
    
    def do_default(self):
        print('Invalid command')

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])

if __name__=='__main__':
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockfd:
        sockfd.connect((host, port))
        MUD(sockfd).cmdloop()
