from itertools import *
class Triangle:
    def __init__(self,*a): self.a=sorted(map(list,a))
    def __abs__(self): 
        a=((self.a[0][0]-self.a[1][0])**2+(self.a[0][1]-self.a[1][1])**2)**0.5
        b=((self.a[1][0]-self.a[2][0])**2+(self.a[1][1]-self.a[2][1])**2)**0.5
        c=((self.a[0][0]-self.a[2][0])**2+(self.a[0][1]-self.a[2][1])**2)**0.5
        p=(a+b+c)/2
        return int(r) if int(r:=(p*(p-a)*(p-b)*(p-c))**0.5)==r else r
    def __bool__(self): return bool(abs(self))
    def __lt__(self,other): return abs(self)<abs(other)
    def __contains__(other,self): return abs(self)==0 or all(other.f(c) for c in self.a)
    def f(self,other): 
        x=[(self.a[t][0]-other[0])*(self.a[(t+1)%3][1]-self.a[t][1])-(self.a[(t+1)%3][0]-self.a[t][0])*(self.a[t][1]-other[1]) for t in range(3)]
        return all(t>=0 for t in x) or all(t<=0 for  t in x)
    def __and__(self,other): 
        if abs(self)*abs(other)==0: return False
        x0=self.a[0][0];xm=self.a[2][0];y0=min(self.a, key=lambda x: x[1])[1];ym=max(self.a, key=lambda x: x[1])[1]
        while y0<=ym:
            while x0<=xm:
                if self.f([x0,y0]) and other.f([x0,y0]): return True
                x0+=0.1
            x0=self.a[0][0];y0+=0.1
        return False
import sys
exec(sys.stdin.read())