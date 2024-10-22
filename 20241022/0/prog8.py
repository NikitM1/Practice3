from itertools import*
print( [f"{v}{h}" for v, h in list(product("abcdefgh", range(1,9)))])