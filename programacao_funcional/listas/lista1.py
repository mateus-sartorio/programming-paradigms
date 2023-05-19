from sys import argv
from functools import reduce

### QUESTAO 1 ###

# a)
def inteiros_ate_n(n: int) -> list[int]:
    return [x for x in range(1, n+1)]

# b)
def inteiros_ate_n_invertido(n: int) -> list[int]:
    return [x for x in reversed(inteiros_ate_n(n))]

# c)
def dobro_ate_n(n: int) -> list[int]:
    return [2*x for x in range(1, n + 1)]

# d)
def dobro_de_n(n: int) -> list[int]:
    return [x for x in range(1, 2*n + 1)]

# e)
def divisiveis_por_3(n: int) -> list[int]:
    return [x for x in range(1, n+1) if x % 3 == 0]

# f)
def dobro_pares_quadrado_impares(n: int) -> list[int]:
    return [2*x if x % 2 == 0 else x*x for x in range(1, n+1)]

# g)
def multiplica(n: int) -> int:
    return reduce(lambda x, y: x*y, range(1, n + 1))

# h)
def soma_impares_subtrai_pares(n: int) -> int:
    return reduce(lambda x, y: x + y if y % 2 != 0 else x - y, range(1, n+1))

# i)
def soma_igual_a_n(n: int) -> list[tuple[int, int]]:
    return [(x, n-x) for x in range(1, n+1) if n-x >= 0]

# j)
def elementos_consecutivos(l: list[int]) -> list[tuple[int, int, int]]:
    return [x for x in zip(l, l[1:], l[2:])]

# k)
def minimax(l: list[int]) -> tuple[int, int]:
    return reduce(lambda x, y: (y, x[1]) if y < x[0] else (x[0], y) if y > x[1] else (x[0], x[1]), l, (l[0], l[0]))


### QUESTAO 2 ###

# a)
def verfica_possibilidade(mov: int, pos: tuple[int, int]) -> bool:
    match mov:
        case 1:
            return True
        case other:
            return False