def travel(n): 
    #for i in range(n): 
       # yield "по кочкам"
    yield from ["по кочкам"]*n
    return "и в яму бух"
def travelwrap(n): 
    x=yield from travel(n)
    yield x