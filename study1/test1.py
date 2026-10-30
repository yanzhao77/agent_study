list1 = [1, 2, 3, 4, 5, 66, 7, 8, 888, 9]
set_tep = set(list1)
list = list(set_tep)
print(f'list1: {list}')

print(f'set_tep: {set_tep}')

print('aa' + 'bb')
print([1, 2, 3] + [4, 5, 6] + ['a' + 'b'])
print((1, 2, 3) + (4, 5, 6) + ('a', 'b'))
# print({1, 2, 3} + {'a', "b"})
print({"name": "zhangsan", "age": 23 } + {'name': "李四", "age": 22})
