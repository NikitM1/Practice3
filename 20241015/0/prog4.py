s=input()
x, y=eval(input())
print(eval(s))
a=x; b=y
print(eval(s, None, {"x":b, "y":a}))