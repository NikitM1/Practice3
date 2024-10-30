def fib(m,n):
    a=[1,1]
    for i in range(2,m+n): a+=[a[i-1]+a[i-2]]
    yield from a[m:m+n]

import sys
exec(sys.stdin.read())