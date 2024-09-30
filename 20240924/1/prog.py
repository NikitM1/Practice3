print([x for x in range(*eval(input())) if x>1 and all(x%d for d in range(2,int(x**0.5)+1))])

