less=lambda a,b: a[0]<=b[0] and a[1]<=b[1] and any(a[i]<b[i] for i in (0,1))

def pareto(*a):
    return tuple([x for i,x in enumerate(a) if all(i==j or not less(x,a[j]) for j in range(len(a)))])
print(pareto(*eval(input())))

