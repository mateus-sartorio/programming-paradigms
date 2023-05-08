:- data_source(personagens,
               sparql("SELECT DISTINCT ?nome ?nomepai ?nomeconjugue
                       WHERE
                       { ?personagem <http://dbpedia.org/ontology/series> <http://dbpedia.org/resource/A_Song_of_Ice_and_Fire>.
                         ?personagem <http://dbpedia.org/property/name> ?nome.
                         
                         ?parente <http://dbpedia.org/ontology/child> ?personagem.
                         ?parente <http://dbpedia.org/ontology/spouse> ?conjugue.
                         ?conjugue <http://dbpedia.org/property/name> ?nomeconjugue.
                         ?parente <http://dbpedia.org/property/name> ?nomepai.
                       }",
                      [ endpoint('https://dbpedia.org/sparql')
                      ])).

personagem(X) :- personagens{nome: X}.
personagem(X) :- personagens{nomepai: X}.
personagem(X) :- personagens{nomeconjugue: X}.
eh_filho(Nome, NomePai) :- personagens{nome: Nome, nomepai: NomePai}.
casados(Conjugue1, Conjugue2) :- personagens{nomepai: Conjugue1, nomeconjugue: Conjugue2}.
bastardo(X) :-
    personagem(X),
    personagem(Y),
    personagem(Z),
    dif(X, Y),
    dif(X, Z),
    dif(Y, Z),
    eh_filho(X, Y),
    \+ eh_filho(X, Z),
    casados(Y, Z).
