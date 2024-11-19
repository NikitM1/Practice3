class Undead(Exception): pass
class Skeleton(Undead): pass
class Zombie(Undead): pass
class Ghoul(Undead): pass
def necro(a): raise Ghoul if a%3==2 else Zombie if a%3 else Skeleton
for a in range(*eval(input())):
    try: necro(a)
    except Skeleton: print('Skeleton')
    except Zombie: print('Zombie')
    except Undead: print('Generic Undead')