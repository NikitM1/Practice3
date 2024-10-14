w=len(input());a={'.':0, '~':0};h=1
while t:=input(): h+=1; a['.']+=t.count('.');a['~']+=t.count('~')

ans=[['#']*h for i in range(w)];a1=a['.']
print(*ans[0],sep='')
for i in range(1,w-1):
    for j in range(1,h-1):
        if a1: a1-=1;ans[i][j]='.'
        else: ans[i][j]='~'
    if ans[i].count('.') and ans[i].count('~'): ans[i]=''.join(ans[i]).replace('.','~')
    print(*ans[i],sep='')
print(*ans[-1],sep='');t=round(a['.']/max(a.values())*20)
print('.'*t,' '*(20-t),' '*(len(str(a['~']))-len(str(a['.'])))+str(a['.'])+'/'+str(a['.']+a['~']));t=t=round(a['~']/max(a.values())*20)
print('~'*t,' '*(20-t),' '*(len(str(a['.']))-len(str(a['~'])))+str(a['~'])+'/'+str(a['.']+a['~']))