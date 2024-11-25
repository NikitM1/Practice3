def objcount(cls):
    cls.counter=0
    old_init=cls.__init__
    def new_init(self,*args):cls.counter+=1;old_init(self,*args)
    cls.__init__ = new_init
    old_del = getattr(cls,'__del__',None)
    def new_del(self):
        cls.counter-=1
        if old_del!=None:old_del(self)
    cls.__del__=new_del
    return cls
import sys
exec(sys.stdin.read())

