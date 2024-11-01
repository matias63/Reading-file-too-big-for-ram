

from tkinter import Y
# composition
def f(x):
    return x+2

def g(h,x):
    return h(x) * 2

print(g(f, 42)) # 88

#closure
def addx(x):
    def _(y):
        return x+y
    return _

add2 = addx(2)
add3 = addx(3)
print(add2(2)) # 4
print(add3(2)) # 5

add3 = addx(3)
print(add3(3)) # 6


# currying
def f(x,y):
    return x*y
def f2(x):
    def _(y):
        return (x,y)
    return _

print(f2(2)) # result is a function

print(f2(2)(3)) # (2,3)
