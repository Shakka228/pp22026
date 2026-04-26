def myfunc(n):
  return len(n)

x = map(myfunc, ('apple', 'banana', 'cherry'))

len("hello")  # 5

len([1,2,3])  # 3

sum([1,2,3])  # 6

min([5,1,9])  # 1
max([5,1,9])  # 9


nums = [1,2,3]
result = map(lambda x: x*2, nums)
print(list(result))


nums = [1,2,3,4]
even = filter(lambda x: x % 2 == 0, nums)
print(list(even))


from functools import reduce
nums = [1,2,3,4]
result = reduce(lambda a,b: a+b, nums)
print(result)
