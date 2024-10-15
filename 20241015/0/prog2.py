from string import ascii_lowercase
from timeit import Timer

s = set(input('String: '))

def lettercount(s): # vowels and consonants
    wov = set("aouiey")
    cons = set(ascii_lowercase) - wov
    return len(s & wov), len(s & cons)

T = Timer("lettercount(s)", globals=globals())
print(T.autorange())