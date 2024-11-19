class InvalidInput(Exception): pass
class BadTriangle(Exception): pass
def triangleSquare(s):
    try: x,y,z=t=eval(s)
    except: raise InvalidInput
    if type(t)!=tuple or len(t)>3 or any(type(c)!=tuple for c in t): raise InvalidInput
    try:
        s=abs((y[0]-x[0])*(z[1]-x[1])-(z[0]-x[0])*(y[1]-x[1]))*0.5
        if s: return s
        else: raise BadTriangle 
    except: raise BadTriangle
s=0
while s==0:
    try: s=triangleSquare(input())
    except InvalidInput: print('Invalid input')
    except BadTriangle: print('Not a triangle')
else: print(s if s-3 else str(s)+'0')