class Dog:
    species = "Canine"

    def __init__(self, name, age):
        self.name = name  
        self.age = age    


dog1 = Dog("Buddy", 3)
dog2 = Dog("Bella", 5)
print(dog1.species) 
print(dog2.species) 

Dog.species = "Dog"
print(dog1.species)  
print(dog2.species) 

dog1.species = "Wolf"
print(dog1.species)  
print(dog2.species)

class Cat:
    count = 0 

    def __init__(self, name):
        self.name = name
        Cat.count += 1 

c1 = Cat("Kitty")
c2 = Cat("Tom")
print(Cat.count)