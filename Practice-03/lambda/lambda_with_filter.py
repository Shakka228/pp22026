numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)

even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)

numbers1 = [1, 3, 5, 7, 9, 2, 4]
greater_than_five = list(filter(lambda x: x > 5, numbers1))
print(greater_than_five)

words = ["hello", "", "world", "", "python"]
non_empty = list(filter(lambda x: x != "", words))
print(non_empty)

numbers2 = [-3, -1, 0, 2, 4, -5]
positive_numbers = list(filter(lambda x: x > 0, numbers2))
print(positive_numbers)