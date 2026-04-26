x = lambda a : a + 10
print(x(5))

x2 = lambda a1, b1 : a1 * b1
print(x2(5, 6))

x1 = lambda a2, b2, c2 : a2 + b2 + c2
print(x1(5, 6, 2))

def myfunc(n):
  return lambda a3 : a3 * n

mydoubler = myfunc(2)

print(mydoubler(11))

def myfunc1(n1):
  return lambda a4 : a4 * n1

mydoubler1 = myfunc1(2)
mytripler = myfunc1(3)

print(mydoubler1(11))
print(mytripler(11))