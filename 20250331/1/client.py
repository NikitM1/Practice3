import cmd
import cowsay
import readline
import shlex
import socket
import sys
import threading

NAMES_LIST=cowsay.list_cows()+['jgsbat']
WEAPON=['sword','spear','axe']

class MUD(cmd.Cmd):
    intro='<<< Welcome to Python-MUD 0.1 >>>'
    prompt='>>>'
    
    def __init__(self,socket):
        super().__init__()
        self.socket=socket
        #self.socket.sendall(b'size\n')
        self.SIZE=10  #int(self.socket.recv(1024).decode())
    
    def do_up(self,args):
        if args: print('Invalid arguments')
        else: 
            self.socket.sendall(b'move 0 -1\n')
    
    def do_down(self,args):
        if args: print('Invalid arguments')
        else: 
            self.socket.sendall(b'move 0 1\n')
    
    def do_left(self,args):
        if args: print('Invalid arguments')
        else: 
            self.socket.sendall(b'move -1 0\n')
    
    def do_right(self,args):
        if args: print('Invalid arguments')
        else: 
            self.socket.sendall(b'move 1 0\n')
    
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
            c.pop(c.index('hello')+1)
            hitpoints=int(c[c.index('hp')+1])
            if hitpoints<=0: raise ValueError
            coords=c.index('coords')
            x,y=int(c[coords+1]),int(c[coords+2]) #if not int then raise ValueError
            if not (0<=x<self.SIZE and 0<=y<self.SIZE): raise ValueError
            self.socket.sendall((shlex.join(['addmon',name,str(hitpoints),str(x),str(y),speech])+'\n').encode())
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
        self.socket.sendall((shlex.join(['attack',args[0],str(10+WEAPON.index(weapon)*5)])+'\n').encode())
    
    def complete_attack(self, text, line, begidx, endidx):
        args = shlex.split(line[:begidx], False, False)
        if args[-1] == 'attack':
            return [c for c in NAMES_LIST if c.startswith(text)]
        elif args[-1]=='with':
            return [c for c in WEAPON if c.startswith(text)]
    
    def do_EOF(self,args):
        self.socket=None
        return 1
    
    def do_default(self):
        print('Invalid command')

def listen(cmdline):
    while cmdline.socket is not None:
        data = b''
        while len(new := cmdline.socket.recv(1024)) == 1024:
            data += new
        data += new
        print(f"\n{data.decode().rstrip()}",
               f"\n{cmdline.prompt}{readline.get_line_buffer()}",
               sep='', end='', flush=True)

host = "localhost" if len(sys.argv) < 3 else sys.argv[2]
port = 1337 if len(sys.argv) < 4 else int(sys.argv[3])

if __name__=='__main__':
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockfd:
        try:
            sockfd.connect((host, port))
        except:
            print('Connection refused')
            exit()
        sockfd.sendall(f"{sys.argv[1]}\n".encode())
        if int(sockfd.recv(1).decode()):
            print(f"Connected to {host}:{port}")
            cmdline = MUD(sockfd)
            listener=threading.Thread(target=listen, args=(cmdline,))
            listener.daemon=True
            listener.start()
            cmdline.cmdloop()
        else:
            print('Connection refused')