class Maze:
    def __init__(self,n):
        self.a=[["█" if i%2==0 or j%2==0 else "·" for i in range(2*n+1)] for j in range(2*n+1)]
    def __str__(self): return '\n'.join(map(''.join,self.a))
    def __setitem__(self,x,v):
        p,q=sorted([(x[1].start,x[0]),(x[2],x[1].stop)])
        if p[0]==q[0]:
            for i in range(p[1]*2+1,q[1]*2+2): self.a[p[0]*2+1][i]="·"
        elif p[1]==q[1]:
            for i in range(p[0]*2+1,q[0]*2+2): self.a[i][p[1]*2+1]="·"
    def __getitem__(self,x):
        p=(x[1].start,x[0]);q=(x[2],x[1].stop)
        return self.possible(tuple(map(lambda x: x*2+1,p)),tuple(map(lambda x: x*2+1,q)),{tuple(map(lambda x: x*2+1,p))})
    def possible(self,p,q,prevs):
        if p==q: return True
        x,y=p
        t=[c for c in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)] if c not in prevs and self.a[c[0]][c[1]]=="·"]
        if t: return any(self.possible(c,q,prevs|{p}) for c in t)
        else: return False
import sys
print(sys.stdin.read())