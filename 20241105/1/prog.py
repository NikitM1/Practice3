class Omnibus:
    d = {}
    def __setattr__(self, name, value):
        Omnibus.d[name]=Omnibus.d[name]|{self} if name in Omnibus.d else {self}
    def __getattr__(self, name):
        return len(Omnibus.d[name])
    def __delattr__(self, name):
        if name in Omnibus.d: Omnibus.d[name].discard(self)
import sys
exec(sys.stdin.read())