male(ahmed).
male(ali).
male(usman).
male(hamza).
male(bilal).

female(fatima).
female(aisha).
female(sara).
female(amna).

parent(ahmed, ali).
parent(fatima, ali).

parent(ahmed, sara).
parent(fatima, sara).

parent(ali, hamza).
parent(aisha, hamza).

parent(ali, amna).
parent(aisha, amna).

parent(sara, bilal).
parent(usman, bilal).
father(X,Y) :- male(X), parent(X,Y).

mother(X,Y) :- female(X), parent(X,Y).

grandparent(X,Z) :- parent(X,Y), parent(Y,Z).

grandfather(X,Z) :- male(X), grandparent(X,Z).

grandmother(X,Z) :- female(X), grandparent(X,Z).

sibling(X,Y) :- parent(Z,X), parent(Z,Y), X \= Y.

brother(X,Y) :- male(X), sibling(X,Y).

sister(X,Y) :- female(X), sibling(X,Y).
