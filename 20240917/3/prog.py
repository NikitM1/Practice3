sumc=lambda x: x%10+sumc(x//10) if x else 0
i=n=int(input())
while i<=n+2:
    j=n
    while j<=n+2:
        print(i,'*',j,'=',i*j if sumc(i*j)!=6 else ':=)',end=' ' if n+2-j else '\n')
        j+=1
    i+=1