# --- Person with greet ---
class Person:
    def __init__(self, name, age=None):
        self.name = name
        self.age = age

    def greet(self):
        print("Hello, my name is " + self.name)

    def get_info(self):
        if self.age is not None:
            return f"{self.name} is {self.age} years old"
        return f"My name is {self.name}"

    def celebrate_birthday(self):
        if self.age is not None:
            self.age += 1
            print(f"Happy birthday! You are now {self.age}")
        else:
            print("Age not set.")

    def __str__(self):
        if self.age is not None:
            return f"Person(name={self.name}, age={self.age})"
        return f"Person(name={self.name})"


# --- Using Person ---
p1 = Person("Emil", 36)
p1.greet()
print(p1.get_info())

p2 = Person("Linus", 25)
p2.celebrate_birthday()
p2.celebrate_birthday()

print(p1)


# --- Calculator Class ---
class Calculator:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b


calc = Calculator()
print(calc.add(5, 3))
print(calc.multiply(4, 7))


# --- Demonstrating method deletion safely ---
class SimplePerson:
    def greet(self):
        print("Hello!")

sp = SimplePerson()
sp.greet()

del SimplePerson.greet  # deleting method from class

# Now calling greet would cause error, so we check first
if hasattr(sp, "greet"):
    sp.greet()
else:
    print("Method greet was deleted.")
