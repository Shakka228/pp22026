# 1️ Generator that generates squares up to N

def square_generator(N):
    for i in range(N + 1):
        yield i * i

print("Squares up to 5:")
for num in square_generator(5):
    print(num)

print("-" * 40)


# 2️ Print even numbers between 0 and n (comma separated)

n = int(input("Enter n for even numbers: "))

even_numbers = (str(i) for i in range(n + 1) if i % 2 == 0)
print("Even numbers:", ",".join(even_numbers))

print("-" * 40)


# 3️ Generator for numbers divisible by 3 and 4 between 0 and n

def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

print("Numbers divisible by 3 and 4 up to 100:")
for num in divisible_by_3_and_4(100):
    print(num)

print("-" * 40)


# 4 Generator squares from a to b

def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

print("Squares from 3 to 7:")
for value in squares(3, 7):
    print(value)

print("-" * 40)


# 5️ Generator from n down to 0

def countdown(n):
    while n >= 0:
        yield n
        n -= 1

print("Countdown from 5:")
for number in countdown(5):
    print(number)