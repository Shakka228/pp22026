# --- Parent class ---
class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname


# --- Student inherits from Person ---
class Student(Person):
    def __init__(self, fname, lname):
        super().__init__(fname, lname)


s = Student("John", "Doe")
print(s.firstname, s.lastname)


# --- Employee / Manager ---
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary


class Manager(Employee):
    def __init__(self, name, salary, bonus):
        super().__init__(name, salary)
        self.bonus = bonus


m = Manager("Alice", 5000, 1000)
print(m.name, m.salary, m.bonus)  # Alice 5000 1000


# --- Vehicle / Car ---
class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model


class Car(Vehicle):
    def __init__(self, brand, model, year):
        super().__init__(brand, model)
        self.year = year


c = Car("Toyota", "Corolla", 2022)
print(c.brand, c.model, c.year)  # Toyota Corolla 2022


# --- Shape / Rectangle (method overriding) ---
class Shape:
    def area(self):
        return 0


class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        base_area = super().area()
        return self.length * self.width + base_area


r = Rectangle(4, 5)
print(r.area())  # 20
