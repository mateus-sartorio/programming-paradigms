:- data_source(personagens,
    sparql(
        "SELECT DISTINCT ?nome ?nomeparente ?nomeconjugue
        WHERE{
            {?personagem <http://dbpedia.org/ontology/series> <http://dbpedia.org/resource/A_Song_of_Ice_and_Fire>.}
            UNION
            {<http://dbpedia.org/resource/List_of_Game_of_Thrones_characters> <http://dbpedia.org/ontology/wikiPageWikiLink> ?personagem.}
                       
            ?personagem <http://dbpedia.org/property/name> ?nome.
                           
            {?parente <http://dbpedia.org/ontology/child> ?personagem.}
            UNION
            {?parente <http://dbpedia.org/property/children> ?personagem.}
            UNION
            {?parente <http://dbpedia.org/ontology/child> ?personagem.}
                       
            {?parente <http://dbpedia.org/ontology/spouse> ?conjugue.}
            UNION
            {?parente <http://dbpedia.org/property/spouses> ?conjugue.}
                       
            ?parente <http://dbpedia.org/property/name> ?nomeparente.
                       
            ?conjugue <http://dbpedia.org/property/name> ?nomeconjugue.
        }",
        [ endpoint('https://dbpedia.org/sparql') ]
    )
).

personagem(X) :- personagens{nome: X}.
personagem(X) :- personagens{nomeparente: X}.
personagem(X) :- personagens{nomeconjugue: X}.

eh_filho(Nome, NomePai) :- personagens{nome: Nome, nomeparente: NomePai}.
casados(Conjugue1, Conjugue2) :- personagens{nomeparente: Conjugue1, nomeconjugue: Conjugue2}.

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

filho_legitimo(X) :-
    personagem(X),
    \+ bastardo(X).