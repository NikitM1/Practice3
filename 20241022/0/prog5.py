from itertools import dropwhile, islice, count
def gen():
   s=0; 
   for i in count(1): 
      s+=1/(i*i)
      yield s
s=0
l=list(islice(dropwhile(lambda x: x<1.6, gen()), 10))
d=list(islice(dropwhile(lambda x: x<1.6, (s:= s+1/(i*i) for i in count(1))), 10))