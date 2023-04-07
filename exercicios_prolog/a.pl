genitor(joana,joao).
genitor(joao,jose).
genitor(joao,maria). 
genitor(jose,ana).
genitor(jose,paulo). 
genitor(maria,pedro).

%% Item 1) %%
irm_(X, Y) :-
    genitor(Z, X),
    genitor(Z, Y),
    dif(X, Y).

%% Item 2) %%
prim_(X, Y) :-
    genitor(W, X),
    genitor(Z, Y),
    irm_(W, Z),
    dif(X, Y).

%% Item 3) %%
net_(X, Y) :-
    genitor(W, X),
    genitor(Y, W),
    dif(X, Y).

%% Item 4) %%
descendente(X, Y) :-
    dif(X, Y),
    (   
    	genitor(Y, X);
    	genitor(Y, Z)
    ).
