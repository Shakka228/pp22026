class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

    def printname(self):
        print(self.firstname, self.lastname)


# Наследование
class Student(Person):
    def __init__(self, fname, lname, graduationyear):
        super().__init__(fname, lname)
        self.graduationyear = graduationyear

    def printinfo(self):
        print(self.firstname, self.lastname, self.graduationyear)


# Создание объектов
x = Person("John", "Doe")
x.printname()

s = Student("Mike", "Olsen", 2019)
s.printname()
s.printinfo()
