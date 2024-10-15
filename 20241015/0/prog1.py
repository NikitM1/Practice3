import timeit

snip=input("Snippet: ")
T=timeit.Timer(snip)
res=T.autorange()
print(res)
