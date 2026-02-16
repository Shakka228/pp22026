class MyClass:
    x = 5  # class variable


p1 = MyClass()
print(p1.x)

p4 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p4.x)
print(p2.x)
print(p3.x)

# deleting object
del p1


class Person:
    pass


class Person4:
    def __init__(self, name2, age2=18):
        self.name2 = name2
        self.age2 = age2


p4 = Person4("Emil")
print(p4.name2, p4.age2)


class Person5:
    def __init__(self, name3, age3, city3, country3):
        self.name3 = name3
        self.age3 = age3
        self.city3 = city3
        self.country3 = country3


p5 = Person5("Linus", 30, "Oslo", "Norway")

print(p5.name3)
print(p5.age3)
print(p5.city3)
print(p5.country3)
