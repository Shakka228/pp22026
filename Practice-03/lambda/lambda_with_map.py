numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

squares = list(map(lambda x: x ** 2, numbers))
print(squares)

strings = ["1", "2", "3", "4"]
ints = list(map(int, strings))
print(ints)

words = ["apple", "banana", "cherry"]
upper_words = list(map(str.upper, words))
print(upper_words)

prices = [100, 250, 400]
with_vat = list(map(lambda x: x * 1.2, prices))
print(with_vat)