from collections import Counter
s1=input().split()
s2=input().split()
c1=Counter(s1)
c2=Counter(s2)
if c1-c2: print("No")
else: print("Awww")