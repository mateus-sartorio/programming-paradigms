from datetime import date
from dateutil.relativedelta import relativedelta
from functools import reduce

############################# QUESTAO 1 #############################

def posicao_valida(p: tuple[int, int]) -> bool:
    if (p[0] >= 1 and p[0] <= 8) and (p[1] >= 1 and p[1] <= 8):
        return True
    else:
        return False

def eh_diagonal(p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    return abs(p2[0] - p1[0]) == abs(p2[1] - p1[1])

def eh_ortogonal(p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    return (p1[0] == p2[0]) or (p1[1] == p2[1])

def faz_o_L(p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    return ((abs(p2[0] - p1[0]) == 1) and (abs(p2[1] - p1[1]) == 2)) or ((abs(p2[0] - p1[0]) == 2) and (abs(p2[1] - p1[1]) == 1))

def possivel_eliminar_de_fato(peca: str, p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    match peca:
        case "rei":
            return (abs(p2[0] - p1[0]) <= 1) and (abs(p2[1] - p1[1]) <= 1)
        case "dama":
            return eh_diagonal(p1, p2) or eh_ortogonal(p1, p2)
        case "torre":
            return eh_ortogonal(p1, p2)
        case "bispo":
            return eh_diagonal(p1, p2)
        case "cavalo":
            return faz_o_L(p1, p2)
        case "peao":
            return (p2[1] == p1[1] + 1) and (abs(p2[0] - p1[0]) == 1)
        case _:
            raise Exception(f"Peça \"{peca}\" invalida.")

def possivel_eliminar(peca: str, p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    if (p1[0] == p2[0]) and (p1[1] == p2[1]):
        raise Exception("A posicao da peca do jogador nao pode ser a mesma da peca alvo")
    elif(posicao_valida(p1) == False):
        raise Exception(f"Posicao invalida do jogador ({p1[0]}, {p1[1]}).")
    elif(posicao_valida(p2) == False):
        raise Exception(f"Posicao invalida da peca alvo ({p2[0]}, {p2[1]}).")
    else:
        # Verifica se eh possivel eliminar a peca e se a posicao resultante da peca do jogador sera valida
        return possivel_eliminar_de_fato(peca, p1, p2)


############################# QUESTAO 2 #############################

def doac1(): return [(36167, 'F', (12, 12, 2010), (21, 9, 1922), 'B', '-', 250),(36167, 'F', (12, 12, 2010), (21, 9, 1922), 'B', '-', 250), (26380, 'F', (12, 6, 2010), (20, 9, 1975), 'A', '+', 500), (15643, 'M', (19, 1, 2010), (5, 6, 1970), 'O', '-', 500), (23872, 'M', (24, 11, 2010), (9, 10, 1984), 'A', '+', 250), ]

def doac2(): return [(36167, 'F', (12, 8, 2010), (21, 9, 1952), 'B', '-', 500), (26380, 'M', (12, 6, 2010), (20, 9, 1975), 'A', '+', 250), (15643, 'M', (19, 1, 2010), (5, 6, 1970), 'O', '-', 500), (23872, 'M', (24, 11, 2010), (9, 10, 1984), 'A', '-', 250), (34332, 'M', (17, 5, 2010), (4, 8, 1959), 'B', '+', 500), (36995, 'F', (27, 3, 2010), (14, 7, 1982), 'A', '-', 250), (23092, 'M', (12, 1, 2010), (13, 1, 1972), 'AB', '+', 500), (18751, 'F', (17, 8, 2010), (2, 10, 1983), 'O', '-', 250), (32278, 'F', (14, 5, 2010), (10, 2, 1950), 'A', '+', 250), (48566, 'F', (23, 9, 2010), (6, 10, 1960), 'O', '-', 500), (44626, 'F', (3, 7, 2010), (21, 2, 1979), 'O', '-', 250), (38154, 'M', (15, 5, 2010), (20, 1, 1984), 'AB', '+', 500), (21516, 'F', (6, 3, 2010), (20, 5, 1980), 'O', '+', 250), (11828, 'F', (28, 1, 2010), (6, 5, 1965), 'AB', '-', 500), (44289, 'M', (21, 10, 2010), (10, 11, 1970), 'O', '-', 500), (10802, 'M', (17, 7, 2010), (15, 4, 1968), 'B', '-', 500), (35589, 'F', (18, 9, 2010), (21, 10, 1972), 'O', '+', 500), (19099, 'F', (2, 4, 2010), (5, 1, 1956), 'AB', '-', 250), (44677, 'M', (26, 3, 2010), (6, 8, 1986), 'AB', '-', 250), (22662, 'M', (4, 4, 2010), (25, 6, 1974), 'O', '+', 500)]

def req1(): return [(1,'A','+',850),(1,'O','+',250),(2,'O','-',500)]

### 1. ###
def doadores_aptos_nova_doacao(doadores: list[tuple[int, str, tuple[int, int, int], tuple[int, int, int], str, str, int]], data_atual: tuple[int, int, int]) -> list[tuple[int, tuple[int, int, int], tuple[int, int, int]]]:
    def tupla_para_date(data: tuple[int, int, int]) -> date:
        return date(data[2], data[1], data[0])

    def idade(data_atual: tuple[int, int, int], nascimento: tuple[int, int, int]) -> int:
        return tupla_para_date(data_atual).year - tupla_para_date(nascimento).year - ((tupla_para_date(data_atual).month, tupla_para_date(data_atual).day) < (tupla_para_date(nascimento).month, tupla_para_date(nascimento).day))

    def tempo_decorrido(data_atual: tuple[int, int, int], dia: tuple[int, int, int]) -> int:
        return (tupla_para_date(data_atual) - tupla_para_date(dia)).days
    
    def apto(doador: tuple[int, str, tuple[int, int, int], tuple[int, int, int], str, str, int]) -> bool:
        if idade(data_atual, doador[3]) >= 60:
            return False
        elif (doador[1] == "F") and (tempo_decorrido(data_atual, doador[2]) >= 90):
            return True
        elif (doador[1] == "M") and (tempo_decorrido(data_atual, doador[2]) >= 60):
            return True
        else:
            return False

    return list(map(lambda x: (x[0], x[2], x[3]), filter(apto, doadores)))

# print(doadores_aptos_nova_doacao(doac1(), (20, 1, 2011)))
# print(doadores_aptos_nova_doacao(doac2(),(20, 1, 2011)))

### 2. ###
def doadores_aptos_nova_doacao_mes(doadores: list[tuple[int, str, tuple[int, int, int], tuple[int, int, int], str, str, int]], mes_atual: tuple[int, int]) -> list[tuple[int, tuple[int, int, int], tuple[int, int, int]]]:
    return doadores_aptos_nova_doacao(doadores, ((date(mes_atual[1], mes_atual[0], 1) + relativedelta(day=31)).day, mes_atual[0], mes_atual[1]))

# print(doadores_aptos_nova_doacao_mes(doac1(),(3, 2010)))
# print(doadores_aptos_nova_doacao_mes(doac2(),(3, 2010)))

### 3. ###
def mais_doacoes_ano(doadores: list[tuple[int, str, tuple[int, int, int], tuple[int, int, int], str, str, int]], ano: int):
    def incrementa_indice(v: list[int], i: int) -> list[int]:
        return list(map(lambda x: x[1] + 1 if x[0] == i else x[1], enumerate(v)))
    
    return list(map(lambda x: x[0] + 1, filter(lambda x: x[1] == (sorted(enumerate(reduce(lambda x, y: incrementa_indice(x, y[2][1]-1), filter(lambda x: x[2][2] == ano, doadores), [0]*12)), key=lambda x: x[1], reverse=True)[0][1]), sorted(enumerate(reduce(lambda x, y: incrementa_indice(x, y[2][1]-1), filter(lambda x: x[2][2] == ano, doadores), [0]*12)), key=lambda x: x[1], reverse=True))))

# print(mais_doacoes_ano(doac1(),2010))
# print(mais_doacoes_ano(doac2(),2010))

### 4. ###
def demanda_tipo_sangue(demanda: list[tuple[int, str, str, int]], hospital: int) -> list[tuple[str, str, int]]:
    def incrementa_demanda(d: list[int], z: tuple[int, str, str, int]) -> list[int]:
        def incrementa_indice(v: list[int], i: int, incremento: int) -> list[int]:
            return list(map(lambda x: x[1] + incremento if x[0] == i else x[1], enumerate(v)))
        
        if z[0] != hospital:
            return d
        elif z[1] == 'A' and z[2] == '+':
            return incrementa_indice(d, 0, z[3])
        elif z[1] == 'A' and z[2] == '-':
            return incrementa_indice(d, 1, z[3])
        elif z[1] == 'B' and z[2] == '+':
            return incrementa_indice(d, 2, z[3])
        elif z[1] == 'B' and z[2] == '-':
            return incrementa_indice(d, 3, z[3])
        elif z[1] == 'AB' and z[2] == '+':
            return incrementa_indice(d, 4, z[3])
        elif z[1] == 'AB' and z[2] == '-':
            return incrementa_indice(d, 5, z[3])
        elif z[1] == 'O' and z[2] == '+':
            return incrementa_indice(d, 6, z[3])
        elif z[1] == 'O' and z[2] == '-':
            return incrementa_indice(d, 7, z[3])
        else:
            return d
    
    def mapeia(e: tuple[int, int]) -> tuple[str, str, int]:
        match e[0]:
            case 0:
                return ('A', '+', e[1])
            case 1:
                return ('A', '-', e[1])
            case 2:
                return ('B', '+', e[1])
            case 3:
                return ('B', '-', e[1])
            case 4:
                return ('AB', '+', e[1])
            case 5:
                return ('AB', '-', e[1])
            case 6:
                return ('O', '+', e[1])
            case 7:
                return ('O', '-', e[1])
            case _:
                raise Exception("Tupla nao fornecida")
    
    return list(map(mapeia, enumerate(reduce(incrementa_demanda, demanda, [0]*8))))

# print(demanda_tipo_sangue(req1(), 1))
# print(demanda_tipo_sangue(req1(), 2))

### 5. ###
def tipos_sang_atendidos(requisicao: list[tuple[int, str, str, int]], hospital: int, doacoes: list[tuple[int, str, tuple[int, int, int], tuple[int, int, int], str, str, int]]) -> list[tuple[str, str, int, int]]:
    def incrementa_oferta(oferta: list[int], doacao: tuple[int, str, tuple[int, int, int], tuple[int, int, int], str, str, int]) -> list[int]:
        def incrementa_indice(v: list[int], i: int, incremento: int) -> list[int]:
            return list(map(lambda x: x[1] + incremento if x[0] == i else x[1], enumerate(v)))
        
        if doacao[4] == 'A' and doacao[5] == '+':
            return incrementa_indice(oferta, 0, doacao[6])
        elif doacao[4] == 'A' and doacao[5] == '-':
            return incrementa_indice(oferta, 1, doacao[6])
        elif doacao[4] == 'B' and doacao[5] == '+':
            return incrementa_indice(oferta, 2, doacao[6])
        elif doacao[4] == 'B' and doacao[5] == '-':
            return incrementa_indice(oferta, 3, doacao[6])
        elif doacao[4] == 'AB' and doacao[5] == '+':
            return incrementa_indice(oferta, 4, doacao[6])
        elif doacao[4] == 'AB' and doacao[5] == '-':
            return incrementa_indice(oferta, 5, doacao[6])
        elif doacao[4] == 'O' and doacao[5] == '+':
            return incrementa_indice(oferta, 6, doacao[6])
        elif doacao[4] == 'O' and doacao[5] == '-':
            return incrementa_indice(oferta, 7, doacao[6])
        else:
            return oferta

    # return list(reduce(incrementa_oferta, doacoes, [0]*8))
    return list(filter(lambda x: x[3] != 0, map(lambda x: (x[0][0], x[0][1], x[1], x[0][2]), zip(demanda_tipo_sangue(requisicao, hospital), list(reduce(incrementa_oferta, doacoes, [0]*8))))))

# print(tipos_sang_atendidos(req1(), 1, doac1()))
# print(tipos_sang_atendidos(req1(), 2, doac1()))
# print(tipos_sang_atendidos(req1(), 1, doac2()))

### 6. ###
def doadores_inaptos_nova_doacao(doacoes: list[tuple[int, str, tuple[int, int, int], tuple[int, int, int], str, str, int]], data_atual: tuple[int, int, int]) -> list[tuple[int, tuple[int, int, int], tuple[int, int, int]]]:
    def tupla_para_date(data: tuple[int, int, int]) -> date:
        return date(data[2], data[1], data[0])

    def idade(data_atual: tuple[int, int, int], nascimento: tuple[int, int, int]) -> int:
        return tupla_para_date(data_atual).year - tupla_para_date(nascimento).year - ((tupla_para_date(data_atual).month, tupla_para_date(data_atual).day) < (tupla_para_date(nascimento).month, tupla_para_date(nascimento).day))

    return list(map(lambda x: (x[0], x[2], x[3]), filter(lambda x: idade(data_atual, x[3]) >= 60, doacoes)))

# print(doadores_inaptos_nova_doacao(doac1(), (20, 1, 2021)))
print(doadores_inaptos_nova_doacao(doac2(), (20, 1, 2021)))