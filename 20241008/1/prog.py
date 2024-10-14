from fractions import *
a=eval(input());s=Fraction(a[0]);ans=Fraction(a[1]);koef_a=a[2];koef_b=a[4+koef_a]
b=a[5+koef_a:][::-1];a=a[3:4+koef_a][::-1]
A=lambda x: Fraction(sum([Fraction(a[i]*x**i) for i in range(koef_a+1)]))
B=lambda x: Fraction(sum([Fraction(b[i]*x**i) for i in range(koef_b+1)]))
print(B(s)!=0 and Fraction(A(s)/B(s))==ans or False)