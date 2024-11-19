from collections import *
class DivStr(UserString):
    def __init__(self,s=''): super().__init__(s)
    def __floordiv__(self,n): t=len(self)//n;return iter([self[i*t:(1+i)*t] for i in range(len(self)//t)])
    def __mod__(self,n): t=len(self)%n;return self[-t:]
    
import sys
exec(sys.stdin.read())