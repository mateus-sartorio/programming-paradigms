# from math import sqrt

# def maiorQue(x, y):
#     return (x, y, x > y)

# def divisaoInt(x, y):
#     return (x//y, x%y)

# def distancia(p1, p2):
#     def dx():
#         return p1[0] - p2[0]
#     
#     def dy():
#         return p1[1] - p2[1]

#     return sqrt(dx()**2 + dy()**2)
    
# print(distancia((0, 0), (3, 4)))
# print(list(range(10)))

# temp1 = [2*x for x in [0, 1, 2]]
# temp2 = [x*y for x in [0, 1, 2] for y in [5, 10]]
# temp3 = [2*x for x in [0, 1, 2] if x >= 1]
# temp4 = [(x, x**2) for x in [2*x for x in [0, 1, 2]]]

# def f(x):
#     return 2*x

# temp5 = [f(x) for x in range(1, 9)]

# print(3 in range(0, 10, 2))
# print(range(0, 10)[-1])
# print(list(range(0, 10))[0:4])

# l1 = list(range(0, 10))
# l2 = l1[:]
# l2[0] = -1
# print(l1)

# def f(x):
#     return 2*x

# temp6 = list(map(f, range(1, 6)))
# print(temp6)

# def f(x):
#     return x % 2 == 0

# print(list(filter(f, range(0, 10))))

# from functools import reduce

# def f(x, y):
#     return x + y

# print(reduce(f, range(1, 4)))

# def my_reduce(f, l, i = None):
#     if len(l) > 1:
#         return f(l[0], l[1:], i)
#     else:
#         return l[0] if i == None else f(l[0], i)

# print(list(map(lambda x: 2*x, range(1, 6))))
# print(list(filter(lambda x: x % 2 == 0, range(1, 6))))
# print(reduce(lambda x, y: x * y, [1, 1, 2, 3], 1))

# print(list(zip(range(1, 6), range(2, 7), range(3, 8))))
# print(list(zip([1, 2, 9], [3, 4], [5, 6])))

# print(list(map(lambda x, y, z: (2*x, 3*y, 4*z), range(1, 9), range(2, 7), range(3, 8))))