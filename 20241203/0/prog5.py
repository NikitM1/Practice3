import inspect 
class C: 
    a: int
    def __init__(self, x): 
        if not isinstance(x, inspect.get_annotation()['a']): 
            raise TypeError
        self.a=x
        
