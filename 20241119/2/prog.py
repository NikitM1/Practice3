class Num:
    def __init__(self):
        self.data = {}
    def __get__(self, key, value):
        return self.data.get(key, 0)
    def __set__(self, key, value):
        if hasattr(value, "real"): self.data[key] = value.real
        elif hasattr(value, "__len__"): self.data[key] = value.__len__()
        else: self.data[key]=0


import sys

exec(sys.stdin.read())