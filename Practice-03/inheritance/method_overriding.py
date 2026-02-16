# --- Employee / Manager ---
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary


class Manager(Employee):
    def __init__(self, name, salary, bonus):
        super().__init__(name, salary)
        self.bonus = bonus

    def show_info(self):
        print(f"Manager {self.name}, Salary: {self.salary}, Bonus: {self.bonus}")


m = Manager("Alice", 5000, 1000)
m.show_info()


# --- Person / Student ---
class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    def __init__(self, name, gpa):
        super().__init__(name)
        self.gpa = gpa

    def student_info(self):
        print(f"Student: {self.name}, GPA: {self.gpa}")


s = Student("Bob", 3.8)
s.student_info()


# --- Shape / Circle ---
import math


class Shape:
    def area(self):
        return 0


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def describe(self):
        print(f"Circle with radius {self.radius}, Area: {self.area():.2f}")


c = Circle(5)
c.describe()
