import math
import sys
import socket

def sqroots(coeffs: str):
    a,b,c=map(float, coeffs.split())

    D=b*b-4*a*c
    if D==0:
        return str(-b/2/a)
    elif D<0:
        return ''
    else:
        return ' '.join([str((-b-D**0.5)/2/a), str((-b+D**0.5)/2/a)])

def sqrootnet(line,sock):
    sock.sendall((line+'\n').encode())
    return sock.recv(128).decode().strip()

if __name__=='__main__':
    match sys.argv:
        case [prog,args]:
            print(sqroots(sys.args))
        case [prog, args, host, port]:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host,int(port)))
                print(sqrootnet(args, s))