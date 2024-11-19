class IsType: 
    def __init__(self, typ): 
        delf.typ=typ
    def __call__(sel, fun): 
        def newfun(*args): 
            if not all(isinstance(arg, self.typ) for arg in args): 
                raise TypeError('Not all')
            return fun(*args)
        return newfun


