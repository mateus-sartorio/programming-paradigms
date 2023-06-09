from SPARQLWrapper import SPARQLWrapper, JSON

#set endpoint
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

sparql.setQuery(
    """
    PREFIX dbp: <https://dbpedia.org/ontology/> 
    SELECT DISTINCT ?personagem
    WHERE {
        ?personagem dbo:series <http://dbpedia.org/resource/A_Song_of_Ice_and_Fire>.
    }        
    """
)

#set return format to JSON
sparql.setReturnFormat(JSON) 

# execute query and returns result in JSON format
results = sparql.query().convert() 

print(results)
