import pickle
class SerCls: 
    def __init__(self):

        self.lst=[i for i in range(100)]
        self.dct={str(i): i for i in range(50)}
        self.num=1
        self.sst="wsedrftgyhjnhbgvfcd"
    def __str__(self): 
        return f"{self.lst}/ {self.dct}/ {self.num}"
ser=SerCls()
s=pickle.dumps(ser)
del ser
ss=pickle.loads(s)
print(ss)
