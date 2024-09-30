f=lambda x=None : print('Hello'+(', '+x if x not in (None,'') else '')+'!')

f()
f('world')