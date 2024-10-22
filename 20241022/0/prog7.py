from itertools import* 
def repeater(seq, n): 
    yield from chain.from_iterable(map(lambda x: repeat(x, n), seq))