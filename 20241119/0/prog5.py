from string import ascii_letters
from pympler.asizeof import asizeof 
class Trad: 
    def __init__(self): 
        for attr in ascii_letters:
            setattr(self, attr, attr)
            
class Slotter: 
    __slots__=tuple(ascii_letters)
    def __init__(self): 
        for attr in ascii_letters: 
            setattr(self, attr, attr)
t=[Trad() for i in range(1000)]
s=[Slotter() for i in range(1000)]