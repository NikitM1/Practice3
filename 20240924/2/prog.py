f=lambda x: (x*x)%100
a=list(eval(input()))
for i in range(len(a)):
    for j in range(i+1,len(a)):
        if f(a[i])>f(a[j]): a[i],a[j]=a[j],a[i]
print(a)