a=[]
while (t:=input()):
    a+=[eval(t)]
if not all([len(e)==len(a) for e in a]):
    print('WAT')
    exit(1)
for i in range(len(a)-1):
    for j in range(i+1,len(a)):
        a[i][j],a[j][i]=a[j][i],a[i][j]
print(*a,sep='\n')
