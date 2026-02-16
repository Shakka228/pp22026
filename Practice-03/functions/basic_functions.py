def my_function():
    print("Hello from a function")

# calling a function
my_function()


# function names (сначала нужно объявить функции)

def calculate_sum():
    print("This is calculate_sum function")

def _private_function():
    print("This is a private function (by convention)")

def myFunction2():
    print("This is myFunction2")

calculate_sum()
_private_function()
myFunction2()


# why we use functions
def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))


# function with pass
def my_function1():
    pass
