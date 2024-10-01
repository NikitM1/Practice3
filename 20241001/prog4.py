def F():
    def fun():
        return x 
    print(">", fun__clousure__[0].cel_contents)
    x=3
    print(">", fun__clousure__[0].cell_contents)
    return fun

res=F() 
res()
#print(res())

