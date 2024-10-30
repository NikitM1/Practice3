from itertools import *
def slide(seq,n):
    i=0
    for t in tee(seq,len(seq)): yield from islice(t,i,n+i);i+=1

import sys
exec(sys.stdin.read())