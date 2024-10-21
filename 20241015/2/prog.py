from math import *;d={};k=0
while (k:=k+1):
    s=input()
    if s[0]==':':
        s=s[1:].split();args=s[1:-1]
        for i,t in enumerate(args): s[-1]=s[-1].replace(t,'args['+str(i)+']')
        d[s[0]]=((lambda t: lambda *args: eval(t))(s[-1]),len(args));continue
    elif s.split()[0]=='quit': print(eval(s.split('quit')[1]).format(len(d)+1,k));break
    else:
        if s.split()[0] not in d: continue
        if d[s.split()[0]][1]==1: print(d[s.split()[0]][0](eval(s[s.find(' ')+1:])))
        else: s=s.split();print(d[s[0]][0](*map(eval,s[1:])))
        