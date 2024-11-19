def istype(typ): 
    def genf(f):
        def newfun(*args): 
            if not all(isinstance(arg, typ) for arg in args ): 
                raise TypeError 
             return f(*args)
         return newfun
    return genf

newf = genf(fun)
print(newf(2,3))

@istype(int)
def simplefun(a, b,c): 
    return a+b+c
