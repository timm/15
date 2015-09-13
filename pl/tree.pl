try(X) :- try(50,-10,X).

try(0,_,_) :- !.
try(N,W0,X) :-
  N1 is N - 1,
  retractall(assumption(_,_,_)),
  ignore(prove(X)),
  worths(W1),
  listing(assumption/3),
  W is max(W0,W1),
  format('~w ',W),
  try(N1,W,X).

assume(X/Y):- assumption(X,Z,_),!,Y=Z.
assume(X/Y):- worth(X,Y,S),
         A=assumption(X,Y,S),
         (assert(A);retract(A),fail).
 
prove(true).
prove((X,Y)) :- prove(X), prove(Y).
prove(X) :- \+ clause(X,_), assume(X).
prove(X) :- assume(X),any(clause(X,Y)),prove(Y).

any(X) :-
 setof(N/X,any1(N,X),L0), beam(L0,L),
 member(_/X,L).

any1(N,X) :- X,score(X,N),bound(X,N).
score(_,N) :- N is -random(10000).
bound(_,_). % mabe cull low scores
beam(L,L).  % maybe cull lower scorers

happy/t  :- rich/t, healthy/t.
healthy/t:- diet/light.
happy/t  :- tranquility /hi.
tranquility/hi :- satiated/t.
satiated/t     :- diet/fatty.
tranquility/hi :- diet/light.

worth(X,Y,Z) :- worth1(X,Y,Z),!.
worth(_,_,0).
	
worth1(tranquility,hi,  4).
worth1(diet,fatty,     -2).
worth1(healthy,t,       1).

worths(W) :- findall(One,assumption(_,_,One),All), sum(All,W).

sum([H|T],S) :- sum(T,H,S).
sum([],S,S).
sum([H|T],S0,S) :- S1 is S0+H, sum(T,S1,S).