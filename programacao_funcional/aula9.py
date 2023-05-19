def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def sumNCubes(n):
    return sum(map(lambda x:x*x*x, range(1, n+1)))

def cria_somador(x):
    def somador(y):
        return x + y
    return somador

soma10a = cria_somador(10)
print(soma10a(5))