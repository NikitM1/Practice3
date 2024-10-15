from collections import Counter
from timeit import Timer

def coun():
    d = {w: 0 for w in text}
    for x in text: d[x]+=1
    return d

def cc(): 
    return Counter(text)

text=input().split()   
print(Timer(coun).autorange())
print(Timer(cc).autorange())