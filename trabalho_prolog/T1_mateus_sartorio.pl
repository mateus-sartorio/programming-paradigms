%% Nome: Mateus Ticianeli Sartoiro %%

%% Tema: Usar inferencia logica para descobrir quis personagens da Cronica do Gelo e Fogo (CGF) sao bastardos %%
% Na Cronica do Gelo e Fogo, alguns dos personagens mais importantes sao bastardos,
% ou seja, sao filhos que os grandes lordes de Westeros tiveram fora de seus casamentos.
% Esses bastardos sao muito mal vistos pela nobreza, e geralmente tem suas jornadas de superaçao,
% em que encontram um proposito, ou uma forma de viver honradamente, apesar da posiçao em que nasceram.
% Na Cronica do Gelo e Fogo, o valor de um personagem esta muito relacionado com a "altura" de seu nascimento.
% Um dos personagens principais da Cronica do Gelo e Fogo se chama Jon Snow, que vai para A Grande Muralha
% defender os reinos dos homens contra os Caminhantes Brancos, mortos vivos criados com magia pelas Criaças da Floresta,
% uma raça exterminada a milhares de anos atras pelos primeiros homens, quandos estes invadiram Westeros.
% Os Caminhantes Brancos foram a forma que as Crianças da Floresta encontraram para que os reinos humanos nunca tivessem
% paz enquanto ainda existissem em Westeros, pois nunca podem ser mortos de fato
% e sempre voltam para atormentar os humanos a cada centenas ou milhares de anos.

% Esta parte do codigo eh responsavel por fazer a consulta a dbpedia para obter os dados %
% Obs: a palavra "parente" foi usada como traducao para "parent" do ingles,
% mesmo nao significando a mesma coisa em portugues, pois torna as queries mais legiveis
:- data_source(personagens,
    sparql(
        "SELECT DISTINCT ?nome ?nomeparente ?nomeconjugue
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
        }",
        [ endpoint('https://dbpedia.org/sparql') ]
    )
).

% O que define um personagem eh se ele aparece no campo de nome, no campo de nomeparente ou no de nomeconjugue %
personagem(X) :- personagens{nome: X}.
personagem(X) :- personagens{nomeparente: X}.
personagem(X) :- personagens{nomeconjugue: X}.

% X eh filho de Y caso alguma tupla tenha X no campo nome e Y no campo nomeparente %
eh_filho(X, Y) :- personagens{nome: X, nomeparente: Y}.

% X e Y sao casados caso exista alguma tupla contendo X como nomeparente e Y como nomeconjugue %
casados(X, Y) :- personagens{nomeparente: X, nomeconjugue: Y}.

% Um personagem X eh bastardo caso ele seja filho de Y, nao seja filho de Z, e Y e Z sejam casados %
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

% Um persongam X eh filho legitimo caso ele nao seja bastardo %
filho_legitimo(X) :-
    personagem(X),
    \+ bastardo(X).

% Ideias de consultas interessantes %
% bastardo(X) -> Retorna todos os personagens que sao bastardos %
% filho_legitimo(X) -> Retorna todos os personagens que sao filhos legitimos %
% casados(X, Y) -> Retorna todos os casais de personagens que sao casados %