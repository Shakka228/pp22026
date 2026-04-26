def my_function(x, y):
  return x + y

result = my_function(5, 3)
print(result)

def my_function1():
  return ["apple", "banana", "cherry"]

fruits = my_function1()
print(fruits[0])
print(fruits[1])
print(fruits[2])

def my_function2():
  return (10, 20)

x, y = my_function2()
print("x:", x)
print("y:", y)

def my_function3(name, /):
  print("Hello", name)

my_function3("Emil")

def my_function4(a, b, /, *, c, d):
  return a + b + c + d

result = my_function4(5, 10, c = 15, d = 20)
print(result)