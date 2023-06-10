from functools import reduce
from itertools import product
from SPARQLWrapper import SPARQLWrapper, JSON

### Observacoes iniciais: ###

# 1. Como a query do meu primeiro trabalho ficou pequena, decidi dividir o segundo trabalho em duas partes independentes: a primeira parte continua com o mesmo tema (e a mesma query): o de identificar quais personagens da Cronica do Gelo e Fogo (CGF) sao bastardos. Ja para a segunda query, decidi fazer uma analise de dados nos filmes do Quentin Tarantino.

# 2. Coloquei as saidas do programa para serem impressas em um arquivo chamado resultados.txt.

# 3. Apesar da palavra parente ter significado diferente na lingua portuguesa, na primeira parte deste trabalho ela foi utilizada para designar tanto pai como mae, de forma similar a palavra 'parent' do ingles.

# 4. Na primeira parte usei o sistema de tipagem do python. No entanto, na segunda parte o sistema de tipagem nao foi usado, pois acabaria adicionando complexidade desnecessaria ao trabalho.

# 5. Nem todas as funcoes criadas foram usadas infelizmente, pois as saidas de algumas delas acabaram ficando muito grandes e iriam poluir o arquivo de saida dos resultados.

# Arquivo usado para impressao dos resultados tanto da parte 1 como da parte 2

f = open('resultados.txt', 'w')


#################### PARTE 1: BASTARDOS DA CRONICA DO GELO E FOGO ####################

# Query que obtem tuplas no formato (personagem, parente, conjugue)
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery(
    """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbp: <http://dbpedia.org/property/>

    SELECT DISTINCT ?nome ?nomeparente ?nomeconjugue
    WHERE {
        # Seleciona o URI de todos os personagens da pagina principal da CGF
        # Seleciona tambem os personagens da pagina da lista de personagens
        # Ao final faz a uniao entre os personagens encontrados nas duas queries
        {?personagem dbo:series dbr:A_Song_of_Ice_and_Fire.}
        UNION
        {dbr:List_of_Game_of_Thrones_characters dbo:wikiPageWikiLink ?personagem.}
        
        # Obtem-se o nome do personagem
        ?personagem dbp:name ?nome.

        # Obtem-se os parentes de cada personagem, de tres fontes diferentes
        # Ao final, junta-se o resultado das tres fontes distintas
        {?parente dbo:child ?personagem.}
        UNION
        {?parente dbp:children ?personagem.}
        UNION
        {?parente dbp:child ?personagem.}

        # Obtem-se o conjugue de cada parente a partir de duas fontes, unindo os resultados ao final     
        {?parente dbo:spouse ?conjugue.}
        UNION
        {?parente dbo:spouses ?conjugue.}

        # Obtem-se o nome de cada parente   
        ?parente dbp:name ?nomeparente.

        # Obtem-se o nome de cada conjugue    
        ?conjugue dbp:name ?nomeconjugue.
    }
    """
)

# Configura o formato de retorno para JSON
sparql.setReturnFormat(JSON) 

# Executa a query e retorna o resultado no formato JSON
resultado = sparql.query().convert() 

# Remove todo o boilerplate do resultado obtido e retorna uma lista de tuplas no formato (personagem, parente, conjugue)
def processa_query(resultado) -> list[tuple[str, str, str]]:
    bindings = resultado['results']['bindings']
    return list(map(lambda x: (x['nome']['value'], x['nomeparente']['value'], x['nomeconjugue']['value']), bindings))

tuplas_processadas = processa_query(resultado)

# Cria um conjunto contendo todos os personagens obtidos
def todos_personagens(tuplas: list[tuple[str, str, str]]) -> set[str]:
    return reduce(lambda x, y: x | {y[0], y[1], y[2]}, tuplas, set())

personagens = todos_personagens(tuplas_processadas)

# Verifica se dois personagens sao casados
def eh_casado(suposto_conjugue1: str, suposto_conjugue2: str, tuplas: list[tuple[str, str, str]]) -> bool:
    for _, c1, c2 in tuplas:
        if (c1 == suposto_conjugue1 and c2 == suposto_conjugue2) or (c1 == suposto_conjugue2 and c2 == suposto_conjugue2):
            return True
    
    return False

# Verifica se um personagem eh filho de outro
def eh_filho(suposto_filho: str, suposto_parente: str, tuplas: list[tuple[str, str, str]]) -> bool:
    for f, p, _ in tuplas:
        if f == suposto_filho and p == suposto_parente:
            return True

    return False

# Cria um conjunto contendo todos os bastardos no conjunto de dados obtidos
def todos_bastardos(tuplas: list[tuple[str, str, str]]) -> set[str]:
    return reduce(lambda x, y: x if eh_filho(y[0], y[2], tuplas) else x | {y[0]}, tuplas, set())

bastardos = todos_bastardos(tuplas_processadas)

f.write('#################### PARTE 1: BASTARDOS DA CRONICA DO GELO E FOGO ####################\n\n')
f.write('Bastardos: ')
f.write(', '.join(bastardos))
f.write('\n\n\n')


#################### PARTE 2: FILMES ESCRITOS POR QUENTIN TARANTINO ####################

# Query que obtem tuplas no formato (titulo, orcamento, lucrou, duracao, escritor, elenco), onde elenco representa um ator ou uma atriz
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery(
    """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbp: <http://dbpedia.org/property/>

    SELECT ?titulo ?orcamento ?lucrou ?duracao ?escritor ?elenco
    WHERE {
        # A unica informacao que foi deixada como obrigatoria par um filme foi seu titulo, pois muitos filmes tinham muitas informacoes faltando
        dbr:Quentin_Tarantino_filmography dbo:wikiPageWikiLink ?filme_id.
        ?filme_id dbp:name ?titulo.

        optional {?filme_id dbo:budget ?orcamento.}
        optional {?filme_id dbo:gross ?lucrou.}
        optional {?filme_id dbo:runtime ?duracao.}
        
        optional {
            ?filme_id dbo:writer ?escritor_id.
            ?escritor_id dbo:birthName ?escritor.
        }
        
        optional {
            ?filme_id dbo:starring ?elenco_id.
            ?elenco_id dbo:birthName ?elenco.
        }
    }
    """
)

# Configura o formato de retorno para JSON
sparql.setReturnFormat(JSON) 

# Executa a query e retorna o resultado no formato JSON
resultado_tarantino = sparql.query().convert()

# Processa a query e retorna uma lista de tuplas no formato (titulo, orcamento, lucrou, duracao, escritor, elenco) 
def processa_query_tarantino(resultado):
    def extrai_valores(x):
        # Converte strings para floats, e valores abaixo de 1e3 sao multiplicados por 1 milhao pois a informacao eh implicita
        def normaliza_valor_monetario(v):
            try:
                if float(v) < 1e3:
                    return float(v)*1e6
                else:
                    return float(v)
            except:
                return float('NaN')
        
        # Converte a duracao para minutos no formato float
        def normaliza_tempo(t):
            try:
                return float(t)/60
            except:
                return float('NaN')
        
        # Faz a normalizacao de cada tupla para facilitar o manuseio dos dados
        return (
            x.get('titulo').get('value'),
            None if x.get('orcamento') is None else normaliza_valor_monetario(x.get('orcamento').get('value')),
            None if x.get('lucrou') is None else normaliza_valor_monetario(x.get('lucrou').get('value')),
            None if x.get('duracao') is None else normaliza_tempo(x.get('duracao').get('value')),
            None if x.get('escritor') is None else x.get('escritor').get('value'),
            None if x.get('elenco') is None else x.get('elenco').get('value')
        )
    bindings = resultado['results']['bindings']
    return list(map(extrai_valores, bindings))

tuplas_processadas_tarantino = processa_query_tarantino(resultado_tarantino)

# Retorna um conjunto contendo todos os filmes do Tarantino obtidos
def todos_filmes(tuplas_processadas_tarantino):
    return reduce(lambda x, y: x | {y[0]}, tuplas_processadas_tarantino, set())

todos_filmes_tarantino = todos_filmes(tuplas_processadas_tarantino)

# Retorna um conjunto de tuplas contendo cada filme e sua duracao (titulo, duracao) para todos os filmes de duracao conhecida
def tuplas_filme_duracao(tuplas_processadas_tarantino):
    return reduce(lambda x, y: x | {(y[0], y[3])}, filter(lambda x: x[3] is not None, tuplas_processadas_tarantino), set())

tuplas_filme_duracao_tarantino = tuplas_filme_duracao(tuplas_processadas_tarantino)

# Retorna os top n filmes de maior duracao no formato (titulo, duracao)
# Caso n seja maior que a quantidade de filmes, retorna todos os filmes e suas duracoes ordenados decrescentemente por duracao
def top_n_filmes_mais_longos(n, tuplas_filme_duracao_tarantino):
    lista_filmes_mais_longos_temporaria = list(sorted(tuplas_filme_duracao_tarantino, key=lambda x: x[1], reverse=True))
    try:
        return lista_filmes_mais_longos_temporaria[0:n]
    except:
        return lista_filmes_mais_longos_temporaria

top_5_filmes_mais_longos_tarantino = top_n_filmes_mais_longos(5, tuplas_filme_duracao_tarantino)

# Retorna um dicionario contendo cada diretor (exceto o proprio Tarantino) e o conjunto de filmes que ajudou a escrever juntamente com o Tarantino
def filmes_escritos_por_escritor(tuplas_processadas_tarantino):
    tuplas_escritor_filme = reduce(lambda x, y: x | {(y[4], y[0])}, filter(lambda x: x[4] is not None and x[4] != 'Quentin Jerome Tarantino', tuplas_processadas_tarantino), set())
    return reduce(lambda x, y: x | {y[0]: {y[1]}} if x.get(y[0]) is None else x | {y[0]: x.get(y[0]) | {y[1]}}, tuplas_escritor_filme, dict())

filmes_escritos_por_escritor_tarantino = filmes_escritos_por_escritor(tuplas_processadas_tarantino)

# Retorna um dicionario contendo cada escritor que ajudou a escrever mais de um filme e a quantidade de filmes que ajudou a escrever
def escritores_que_escreveram_mais_de_um_filme(filmes_escritos_por_escritor_tarantino):
    return list(sorted(list(map(lambda x: (x[0], len(x[1])), (filter(lambda x: len(x[1]) > 1, filmes_escritos_por_escritor_tarantino.items())))), key=lambda x: x[1], reverse=True))

escritores_que_escreveram_mais_de_um_filme_do_tarantino = escritores_que_escreveram_mais_de_um_filme(filmes_escritos_por_escritor_tarantino)

# Retorna um dicionario contendo cada ator e o conjunto de filmes em que atuou
def filmes_atuados_por_ator(tuplas_processadas_tarantino):
    tuplas_ator_filme = reduce(lambda x, y: x | {(y[5], y[0])}, filter(lambda x: x[5] is not None, tuplas_processadas_tarantino), set())
    return reduce(lambda x, y: x | {y[0]: {y[1]}} if x.get(y[0]) is None else x | {y[0]: x.get(y[0]) | {y[1]}}, tuplas_ator_filme, dict())

filmes_atuados_por_ator_tarantino = filmes_atuados_por_ator(tuplas_processadas_tarantino)

# Retorna uma lista contendo os n atores que mais atuarem em filmes em ordem decrescente de filmes atuados
def atores_que_atuaram_em_mais_filmes(n, filmes_atuados_por_ator_tarantino):
    lista_atores_com_mais_papeis_temporaria =  list(sorted(list(map(lambda x: (x[0], len(x[1])), filmes_atuados_por_ator_tarantino.items())), key=lambda x: x[1], reverse=True))
    try:
        return lista_atores_com_mais_papeis_temporaria[0:n]
    except:
        return lista_atores_com_mais_papeis_temporaria

top_5_atores_que_atuaram_em_mais_filmes_tarantino = atores_que_atuaram_em_mais_filmes(5, filmes_atuados_por_ator_tarantino)

# Retorna uma lista contendo tuplas de tuplas de atores e o conjunto de filmes em que atuaram juntos
def aturam_juntos(filmes_atuados_por_ator_tarantino):
    return list(filter(lambda x: x[1] != set(), map(lambda x: (x, filmes_atuados_por_ator_tarantino[x[0]].intersection(filmes_atuados_por_ator_tarantino[x[1]])), filter(lambda x: x[0] != x[1], product(filmes_atuados_por_ator_tarantino.keys(), filmes_atuados_por_ator_tarantino.keys())))))

aturam_juntos_em_filmes_do_tarantino = aturam_juntos(filmes_atuados_por_ator_tarantino)

# Retorna uma lista contendo as tuplas de pares de atores que atuaram em pelo menos n filmes do Tarantino juntos e os filmes em que aturam
# A lista eh ordenada em ordem de quantidade de filmes em que um par de atores atuou juntos
def atuaram_juntos_em_pelo_menos_n_filmes(n, aturam_juntos_em_filmes_do_tarantino):
    return list(sorted(filter(lambda x: len(x[1]) >= n, aturam_juntos_em_filmes_do_tarantino), key=lambda x: x[1], reverse=True))

atuaram_juntos_em_pelo_menos_3_filmes_do_tarantino = atuaram_juntos_em_pelo_menos_n_filmes(3, aturam_juntos_em_filmes_do_tarantino)

# Retorna o conjunto de filmes e a quantide de dinheiro gasto para faze-lo, o quanto ele fez nas bilheterias e o saldo top_3_filmes_mais_longos_tarantino
# Filmes com informacoes monetarias desconhecidas sao descartados
def informacao_monetaria_filmes(tuplas_processadas_tarantino):
    return reduce(lambda x, y: x | {(y[0], y[1], y[2], y[2] - y[1] if y[1] is not None and y[2] is not None else None)}, tuplas_processadas_tarantino, set())

informacao_monetaria_filmes_tarantino = informacao_monetaria_filmes(tuplas_processadas_tarantino)

# Retorna uma lista dos filmes que lucraram
def filmes_que_lucraram(informacao_monetaria_filmes_tarantino):
    return list(filter(lambda x: x[3] > 0, reduce(lambda x, y: x | {y} if y[3] is not None else x, informacao_monetaria_filmes_tarantino, set())))

filmes_que_lucraram_tarantino = filmes_que_lucraram(informacao_monetaria_filmes_tarantino)

# Retorna uma lista dos filmes que deram prejuizo
def filmes_que_deram_prejuizo(informacao_monetaria_filmes_tarantino):
    return list(filter(lambda x: x[3] < 0, reduce(lambda x, y: x | {y} if y[3] is not None else x, informacao_monetaria_filmes_tarantino, set())))

filmes_que_deram_prejuizo_tarantino = filmes_que_deram_prejuizo(informacao_monetaria_filmes_tarantino)

# Retorna o orcamento medio dos filmes que se tem informacoes monetarias
def orcamento_medio_filmes(informacao_monetaria_filmes_tarantino):
    filmes_com_orcamento_conhecido = set(filter(lambda x: x[1] is not None, informacao_monetaria_filmes_tarantino))
    return reduce(lambda x, y: x + y[1], filmes_com_orcamento_conhecido, 0)/len(filmes_com_orcamento_conhecido)

orcamento_medio_filmes_tarantino = orcamento_medio_filmes(informacao_monetaria_filmes_tarantino)

# Retorna o valor medio arrecadado nas bilheterias dos filmes que se tem informacoes monetarias
def valor_arrecadado_medio_filmes(informacao_monetaria_filmes_tarantino):
    filmes_com_valor_arrecadado_conhecido = set(filter(lambda x: x[2] is not None, informacao_monetaria_filmes_tarantino))
    return reduce(lambda x, y: x + y[2], filmes_com_valor_arrecadado_conhecido, 0)/len(filmes_com_valor_arrecadado_conhecido)

valor_arrecadado_medio_filmes_tarantino = valor_arrecadado_medio_filmes(informacao_monetaria_filmes_tarantino)

# Retorna o lucro medio dos filmes que se tem informacoes monetarias
def lucro_medio_filmes(informacao_monetaria_filmes_tarantino):
    filmes_com_lucro_conhecido = set(filter(lambda x: x[3] is not None, informacao_monetaria_filmes_tarantino))
    return reduce(lambda x, y: x + y[3], filmes_com_lucro_conhecido, 0)/len(filmes_com_lucro_conhecido)

lucro_medio_filmes_tarantino = lucro_medio_filmes(informacao_monetaria_filmes_tarantino)

# Retorna uma lista contendo os top n filmes mais lucrativos do Tarantino
# Todos os filmes sao retornados em ordem decrescente de lucro caso n seja maior que a quantidade de filmes
def top_n_filmes_mais_lucrativos(n, informacao_monetaria_filmes_tarantino):
    lista_temporaria_filmes_mais_lucrativos = list(map(lambda x: (x[0], x[3]), list(sorted(filter(lambda x: x[3] is not None, informacao_monetaria_filmes_tarantino), key=lambda x: x[3], reverse=True))))
    try:
        return lista_temporaria_filmes_mais_lucrativos[0:n]
    except:
        return lista_temporaria_filmes_mais_lucrativos

top_5_filmes_mais_lucrativos_tarantino = top_n_filmes_mais_lucrativos(5, informacao_monetaria_filmes_tarantino)

# Retorna uma lista contendo os top n filmes que mais deram prejuizo do Tarantino
# Todos os filmes sao retornados em ordem decrescente de lucro caso n seja maior que a quantidade de filmes
def top_n_filmes_que_deram_mais_prejuizo(n, informacao_monetaria_filmes_tarantino):
    lista_temporaria_filmes_que_deram_mais_prejuizo = list(map(lambda x: (x[0], x[3]), list(sorted(filter(lambda x: x[3] is not None, informacao_monetaria_filmes_tarantino), key=lambda x: x[3], reverse=False))))
    try:
        return lista_temporaria_filmes_que_deram_mais_prejuizo[0:n]
    except:
        return lista_temporaria_filmes_que_deram_mais_prejuizo

top_5_filmes_que_deram_mais_prejuizo = top_n_filmes_que_deram_mais_prejuizo(5, informacao_monetaria_filmes_tarantino)


f.write('#################### PARTE 2: FILMES ESCRITOS POR QUENTIN TARANTINO ####################\n\n')

f.write('Top 5 filmes mais longos:\n')
f.write('\n'.join(map(lambda x: f'{x[0] + 1}: {x[1][0]} - {int(x[1][1])} min', enumerate(top_5_filmes_mais_longos_tarantino))))
f.write('\n\n')

f.write('Outros escritores que participaram da criacao dos roteiros dos filmes:\n')
f.write('\n'.join(map(lambda x: f"- {x[0]}: {', '.join(x[1])}", filmes_escritos_por_escritor_tarantino.items()
)))
f.write('\n\n')

f.write('Duplas de atores que atuaram juntos em pelo menos tres filmes do Tarantino:\n')
f.write('\n'.join(map(lambda x: f"- {x[0][0]} e {x[0][1]} - {', '.join(x[1])}", atuaram_juntos_em_pelo_menos_3_filmes_do_tarantino
)))
f.write('\n\n')

f.write('Top 5 atores que apareceram em mais filmes do Tarantino:\n')
f.write('\n'.join(map(lambda x: f'{x[0] + 1}: {x[1][0]} - {x[1][1]}', enumerate(top_5_atores_que_atuaram_em_mais_filmes_tarantino))))
f.write('\n\n')

f.write('Orcamento medio dos filmes do Tarantino:\n')
f.write(f'US$ {int(orcamento_medio_filmes_tarantino/1e6)} milhoes')
f.write('\n\n')

f.write('Valor arrecadado medio dos filmes do Tarantino:\n')
f.write(f'US$ {int(valor_arrecadado_medio_filmes_tarantino/1e6)} milhoes')
f.write('\n\n')

f.write('Lucro medio dos filmes do Tarantino:\n')
f.write(f'US$ {int(lucro_medio_filmes_tarantino/1e6)} milhoes')
f.write('\n\n')

f.write('Top 5 filmes mais lucrativos do Tarantino:\n')
f.write('\n'.join(map(lambda x: f'{x[0] + 1}: {x[1][0]} - US$ {int(x[1][1]/1e6)} milhoes', enumerate(top_5_filmes_mais_lucrativos_tarantino))))
f.write('\n\n')

f.write('Top 5 filmes do Tarantino que deram mais prejuizo:\n')
f.write('\n'.join(map(lambda x: f'{x[0] + 1}: {x[1][0]} - US$ {int(x[1][1]/1e6)} milhoes', enumerate(top_5_filmes_que_deram_mais_prejuizo))))


f.close()
