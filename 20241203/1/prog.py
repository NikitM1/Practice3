class dump(type):
    def __new__(cls, name, bases, dct):
        for attr, value in dct.items():
            if callable(value):
                dct[attr] = cls.wrap_method(value)
        return super().__new__(cls, name, bases, dct)
    
    @staticmethod
    def wrap_method(method):
        def wrapped(self, *args, **kwargs):
            method_name = method.__name__
            print(f"{method_name}: {args}, {kwargs}")
            return method(self, *args, **kwargs)
        return wrapped

import sys
exec(sys.stdin.read())
