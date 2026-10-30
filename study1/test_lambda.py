import functools


def get_sum(a, b):
    return a + b


my_get_sum = lambda a, b: a + b * 2
print(my_get_sum(1, 2))

'''
定义匿名函数
'''


def my_func(a, b, fn):
    return fn(a, b)


print(my_func(1, 2, lambda a, b: a - b))
