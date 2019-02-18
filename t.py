from sympy import *
import numpy as np
init_printing(use_unicode=True)

a = Matrix([[2/3, 2**100], [5, 1]])
c = Matrix(np.random.randint(0, 100, (3,3)))
b = a**-1
print(b)
print(a*b)
print(2*a)
print(c)