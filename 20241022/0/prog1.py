from itertools import count
def gen():
   s=0; #i=1
   #while 1: 
      #s+=1/(i*i)
      #i+=1
      #yield s
   for i in count(1): 
      s+=1/(i*i)
      yield s
      