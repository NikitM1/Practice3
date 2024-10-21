w=int(input());s=''
while t:=input(): s+=t
s=s.lower()
for c in s:
    if not c.isalpha(): s=s.replace(c,' ')
d={t: s.count(t) for t in {v for v in s.split() if len(v)==w}}
print(*sorted(x for x in d if d[x]==max(d.values())))