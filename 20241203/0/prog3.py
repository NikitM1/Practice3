while s:=input(): 
    match s.split(): 
        case ["mov", *r1, r2 ]: 
            print("moving", r1, r2)
        case [('push' | 'pop') as cmd, *tail] if len(tail)>0: 
            print(cmd+'ing', *tail, sep=' ')
        case [md, r1]: 
            print('making', md, 'with', r1)
        case [_]: 
            print('Parse error')
