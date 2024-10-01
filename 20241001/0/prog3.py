from math import*
def MINF(*f):  
        return lambda x :  min( k(x) for k in f) 

res=MINF(sin, cos)
res(pi)
