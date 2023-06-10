from functools import reduce
from SPARQLWrapper import SPARQLWrapper, JSON

### Observacoes iniciais: ###

# 1. Como a query do meu primeiro trabalho ficou pequena, decidi dividir o segundo trabalho em duas partes independentes: a pŕimeira parte continua com o mesmo tema (e a mesma query): o de identificar quais personagens da Cronica do Gelo e Fogo (CGF) sao bastardos. Ja a segunda query TODO colocar o tema da segunda query aqui.

# 2. Coloquei as saidas do programa para serem impressas em um arquivo chamado resultados.txt.

# 3. Apesar da palavra parente ter significado diferente na lingua portuguesa, neste trabalho ela foi utilizada para designar tanto pai como mae, de forma similar a palavra 'parent' do ingles.


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


#################### PARTE 2: BASTARDOS DA CRONICA DO GELO E FOGO ####################

# Query que obtem tuplas no formato (personagem, parente, conjugue)
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery(
    """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbp: <http://dbpedia.org/property/>

    SELECT ?titulo ?orcamento ?lucrou ?duracao ?escritor ?elenco
    WHERE {
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

def processa_query_tarantino(resultado) -> list[tuple[str, str, str, str, str, str]]:
    def extrai_valores(x):
        def normaliza_valor_monetario(v: str) -> float:
            try:
                if float(v) < 1e6:
                    return float(v)*1e6
                else:
                    return float(v)
            except:
                return float('NaN')

        def normaliza_tempo(t: str):
            try:
                return float(t)/60
            except:
                return float('NaN')

        return (
            None if x.get('titulo') is None else x.get('titulo').get('value'),
            None if x.get('orcamento') is None else normaliza_valor_monetario(x.get('orcamento').get('value')),
            None if x.get('lucrou') is None else normaliza_valor_monetario(x.get('lucrou').get('value')),
            None if x.get('duracao') is None else normaliza_tempo(x.get('duracao').get('value')),
            None if x.get('escritor') is None else x.get('escritor').get('value'),
            None if x.get('elenco') is None else x.get('elenco').get('value')
        )
    bindings = resultado['results']['bindings']
    return list(map(extrai_valores, bindings))

tuplas_processadas_tarantino = processa_query_tarantino(resultado_tarantino)

for i in tuplas_processadas_tarantino:
    print(i)
