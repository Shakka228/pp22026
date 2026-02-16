def my_function(*kids):
  print("The youngest child is " + kids[2])

my_function("Emil", "Tobias", "Linus")

def my_function1(*args):
  print("Type:", type(args))
  print("First argument:", args[0])
  print("Second argument:", args[1])
  print("All arguments:", args)

my_function1("Emil", "Tobias", "Linus")

def my_function2(greeting, *names):
  for name in names:
    print(greeting, name)

my_function2("Hello", "Emil", "Tobias", "Linus")

def my_function3(*numbers):
  total = 0
  for num in numbers:
    total += num
  return total

print(my_function3(1, 2, 3))
print(my_function3(10, 20, 30, 40))
print(my_function3(5))

def my_function4(**kid):
  print("His last name is " + kid["lname"])

my_function4(fname = "Tobias", lname = "Refsnes")

def my_function5(**myvar):
  print("Type:", type(myvar))
  print("Name:", myvar["name"])
  print("Age:", myvar["age"])
  print("All data:", myvar)

my_function5(name = "Tobias", age = 30, city = "Bergen")