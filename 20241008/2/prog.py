from math import *
def show(screen): 
    print("\n".join(["".join(s) for s in screen[::-1]]))
def scale(a, b, A, B, x): 
    return ((x-a)*(B-A))/(b-a) + A
 
st=input().split()
w,h,a,b=map(int,st[:-1])
f=lambda x: eval(st[-1])

mx=mn=f(a);i=a+0.05
while i<=b: mx=max(mx,f(i));mn=min(mn,f(i));i+=0.05
screen=[[" "]* w for i in range(h)]
for i in range(w): 
    x=scale(0, w-1, a, b, i)
    y=f(x)
    s=scale(mn, mx, 0, h-1, y)
    #print(len(screen),s)
    screen[round(s)][i]="*"
    if i and abs(prev-round(s))-1:
        if prev<=round(s):
            for j in range(prev+1,round(s)): screen[j][i-1]='*'
        else:
            for j in range(round(s)+1,prev): screen[j][i-1]='*'
    prev=round(s)
show(screen)