class Father:
    def skills(self):
        print("Father: Gardening")

class Mother:
    def skills(self):
        print("Mother: Cooking")

class Child(Father, Mother):
    pass

c = Child()
c.skills() 

class Father:
    def skills(self):
        return "Gardening"

class Mother:
    def skills(self):
        return "Cooking"

class Child(Father, Mother):
    def all_skills(self):
        return f"{Father.skills(self)}, {Mother.skills(self)}"

c = Child()
print(c.all_skills())

class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")

class C(A):
    def show(self):
        print("C")

class D(B, C):
    pass

d = D()
d.show() 

class A:
    def greet(self):
        print("Hello from A")

class B(A):
    def greet(self):
        super().greet()
        print("Hello from B")

class C(A):
    def greet(self):
        super().greet()
        print("Hello from C")

class D(B, C):
    def greet(self):
        super().greet()
        print("Hello from D")

d = D()
d.greet()

from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass

class Dog(Animal):
    def make_sound(self):
        print("Woof!")

class Cat(Animal):
    def make_sound(self):
        print("Meow!")

d = Dog()
d.make_sound()

c = Cat()
c.make_sound() 