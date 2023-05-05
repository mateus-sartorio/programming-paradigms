from math import sqrt

def maiorQue(x, y):
    return (x, y, x > y)

def divisaoInt(x, y):
    return (x//y, x%y)

def distancia(p1, p2):
    def dx():
        return p1[0] - p2[0]
    
    def dy():
        return p1[1] - p2[1]

    return sqrt(dx()**2 + dy()**2)
    
# print(distancia((0, 0), (3, 4)))
# print(list(range(10)))

temp1 = [2*x for x in [0, 1, 2]]
temp2 = [x*y for x in [0, 1, 2] for y in [5, 10]]
temp3 = [2*x for x in [0, 1, 2] if x >= 1]
print(temp3)
