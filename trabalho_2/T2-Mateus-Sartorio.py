from SPARQLWrapper import SPARQLWrapper, JSON

#set endpoint
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

sparql.setQuery(
    """SELECT DISTINCT ?nome ?nomeparente ?nomeconjugue
    WHERE{
        # Seleciona o URI de todos os personagens da pagina principal da CGF
        # Seleciona tambem os personagens da pagina da lista de personagens
        # Ao final faz a uniao entre os personagens encontrados nas duas queries
        {?personagem <http://dbpedia.org/ontology/series> <http://dbpedia.org/resource/A_Song_of_Ice_and_Fire>.}
        UNION
        {<http://dbpedia.org/resource/List_of_Game_of_Thrones_characters> <http://dbpedia.org/ontology/wikiPageWikiLink> ?personagem.}
        
        # Obtem-se o nome do personagem
        ?personagem <http://dbpedia.org/property/name> ?nome.

        # Obtem-se os parentes (parents) de cada personagem, de tres fontes diferentes
        # Ao final, junta-se o resultado das tres fontes distintas    
        {?parente <http://dbpedia.org/ontology/child> ?personagem.}
        UNION
        {?parente <http://dbpedia.org/property/children> ?personagem.}
        UNION
        {?parente <http://dbpedia.org/ontology/child> ?personagem.}

        # Obtem-se o conjugue de cada parente a partir de duas fontes, unindo os resultados ao final     
        {?parente <http://dbpedia.org/ontology/spouse> ?conjugue.}
        UNION
        {?parente <http://dbpedia.org/property/spouses> ?conjugue.}

        # Obtem-se o nome de cada parente   
        ?parente <http://dbpedia.org/property/name> ?nomeparente.

        # Obtem-se o nome de cada conjugue    
        ?conjugue <http://dbpedia.org/property/name> ?nomeconjugue.
    }"""
)

#set return format to JSON
sparql.setReturnFormat(JSON) 

# execute query and returns result in JSON format
results = sparql.query().convert() 

print(results)
