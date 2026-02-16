class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Emil", 36)

print(p1.name)
print(p1.age)


class Person2:
  pass

p2 = Person2()
p2.name6 = "Tobias"
p2.age6 = 25

print(p2.name6)
print(p2.age6)


class Person3:
  def __init__(self, name1, age1):
    self.name1 = name1
    self.age1 = age1

p3 = Person3("Linus", 28)

print(p3.name1)
print(p3.age1)


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
