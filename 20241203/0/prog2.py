class Doubleton(type): 
    _instance=None
    _instance1=None
    n=0
    def __call__(cls, **args, **kw): 
        if cls._instance is None: 
            cls._instance=super().__call__(*args, **kw)
            return cls._instance
        elif cls._instance1 is None: 
            cls._instance=super().__cal__(*args **kw)
            cls.n=1
        else : 
            if cls.n%2 :
                cls.n+=1
                return cls._instance
            else:
                cls.n+=1
                return cls._instance1

