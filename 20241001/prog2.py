l=list(map(int, input().split(',')))
print(*sorted(l, key= lambda x: x**2%100), sep=',')
