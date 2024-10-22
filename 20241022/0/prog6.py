from  itertools import *
def f(s, n):
    return list(filterfalse(lambda x: x%n, s))