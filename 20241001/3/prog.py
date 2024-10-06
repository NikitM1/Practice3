from math import *
Calc = lambda s,t,u: lambda x: eval(u.replace('x',str(eval(s))).replace('y',str(eval(t))))
print(Calc(*eval(input()))(eval(input())))

