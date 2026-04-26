def my_function(fname):
  print(fname + " Refsnes")

my_function("Emil")
my_function("Tobias")
my_function("Linus")

#parameter vs argument
def my_function1(name): # name is a parameter
  print("Hello", name)

my_function1("Emil") # "Emil" is an argument

#num of arg
def my_function2(fname, lname):
  print(fname + " " + lname)

my_function2("Emil", "Refsnes")

#default
def my_function3(name = "friend"):
  print("Hello", name)

my_function3("Emil")
my_function3("Tobias")
my_function3()
my_function3("Linus")

def my_function4(country = "Norway"):
  print("I am from", country)

my_function4("Sweden")
my_function4("India")
my_function4()
my_function4("Brazil")

def my_function5(fruits):
  for fruit in fruits:
    print(fruit)

my_fruits = ["apple", "banana", "cherry"]
my_function5(my_fruits)