f=lambda x,y: type(y)(t for t in x if t not in set(y)) if type(y) in (list,tuple) else x-y
print(f(*eval(input())))

