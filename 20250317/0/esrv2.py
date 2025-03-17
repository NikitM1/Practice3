import cmd
import sys
import socket


class netcat(cmd.Cmd):
    prompt="esrv>"
    
    def response(self):
        print(self.socket.recv(1024).rstrip().decode())
        
    def __init__(self, *ap, socket=None, **kwargs):
        self.socket=socket
        super.__init__(*ap, **kwargs)
    
    def do_print(self,arg):
        self.socket.sendall(f"print {arg}".encode())
        self.response()
    
    def do_info(self,arg):
        self.socket.sendall(f"info {arg}".encode())
        self.response()
    
    def do_EOF(self,arg):
        return 1

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])