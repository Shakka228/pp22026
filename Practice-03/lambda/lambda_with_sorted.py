students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

sorted_by_name = sorted(students, key=lambda x: x[0])
print(sorted_by_name)

numbers = [5, 2, 9, 1, 7]
sorted_numbers = sorted(numbers, reverse=True)
print(sorted_numbers)

words = ["apple", "kiwi", "banana", "fig"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)

names = ["anna", "Bob", "charlie", "alice"]
sorted_names = sorted(names, key=lambda x: x.lower())
print(sorted_names)