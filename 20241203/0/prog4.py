class C: 
    a, b, c = input().split() 
while ss:=input():
    match ss.split(): 
        case [C.a, _] as words if 'yes' in words:
            res='1'
        case [C.b]: 
            res='2'
        case [C.c, _, C.b]: 
            res='3'
        case _: 
            res=None
    if res: print(res)
