st=input().lower();s=set()
for i in range(1,len(st)):
    if st[i-1].isalpha() and st[i].isalpha(): s|={st[i-1]+st[i]}
print(len(s))
    