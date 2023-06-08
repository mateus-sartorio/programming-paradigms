# a = set([1, 2, 3, 3])
# print(a)

# a = dict([('jan', 1), ('fev', 2)])
# print(a)

# print(tuple(iter([1, 2, 3])))

def proximos(it):
    return [next(it), next(it), next(it)]

# print(proximos(iter([1, 2, 3, 4])))


