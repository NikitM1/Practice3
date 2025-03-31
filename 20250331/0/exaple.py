""" This is module."""
import sys
from math import *

"""Some function."""
def thefun(a, b, c): 
    return int(a)+int(b)+sin(int(c))

l = sys.argv[1]
a = b = l
print(thefun(a, b, l))

