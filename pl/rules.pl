stagger(X):-
  bagof(X,clause(X,fact),L),
  rone(X,L).
  
rone(X,L) :- rone(X,_,L).
rone(X,Rest,L) :- length(L,N), rmember1(L,N,X,Rest).

rmember1([H],_,H,[])   :- !.
rmember1([H|T],N,X,Rest) :-
        Pos is random(N) + 1,
        lessN(Pos,Y,[H|T],L),
        ( X=Y,
          Rest=L
        ; Rest=[Y|Rest1],
          N1 is N - 1,
          rmember1(L,N1,X,Rest1)).

lessN(1,H,[H|T],T) :- !.
lessN(N0,X,[H|T],[H|L]) :-  N is N0 - 1, lessN(N,X,T,L).

term_expansion(
  (ask=What,Txt=Options),
  ask(What,Options,Txt)).

:- op(999,xfx,if).
:- op(998,xfx,then).
:- op(995,xfy,or).
:- op(994,xfy,and).
:- op(701,xfx,cf).
:- op(1,fx,rule).

prove(Z):- prove(Z,[],_).

prove(Y is Z,W,W):- 
  member(Y is Z,W).
prove(Y is Z,W,[Y is Z|W]) :-
  \+ member(Y is Z,W),
  ask(Y,Options,_),
  rone(Z,Options).
  
prove(Y is Z,W0,W) :-
  stagger(rule _ if X then Y is Z cf _),
  prove(X,[Y is Z|W0],W).

prove(X and Y) --> prove(X), prove(Y).
prove(X or Y) --> prove(X); prove(Y).
   
rule 1 
  if    nostrils is external_tubular and
        live is at_sea and
        bill is hooked 
  then  order is tubenose cf 80.

rule 2 
  if    feet is webbed and
        bill is flat 
  then  order is waterfowl cf 80.

rule 3 
  if    eats is meat and
        feet is curved_talons and
        bill is sharp_hooked 
  then  order is falconiforms cf 80.

rule 4 
  if    feet is one_long_backward_toe 
  then  order is passerformes cf 80.

rule 5
  if    order is tubenose and
        size is large and
        wings is long_narrow 
  then  family is albatross cf 80.

rule 6 
  if    order is waterfowl and
        neck is long and
        color is white and
        flight is ponderous 
  then  family is swan cf 80.

rule 7
  if    order is waterfowl and
        size is plump and
        flight is powerful 
  then  family is goose cf 80.

rule 8
  if    order is waterfowl and
        feed is on_water_surface and
        flight is agile 
  then  family is duck cf 80.

rule 9 
  if    order is falconiforms and
        feed is scavange and
        wings is broad 
  then  family is vulture cf 80.

rule 10
  if    order is falconiforms and
        wings is long_pointed and
        head is large and
        tail is narrow_at_tip 
  then  family is falcon cf 80.

rule 11
  if    order is passerformes and
        bill is flat and
        eats is flying_insects 
  then  family is flycatcher cf 80.

rule 12
  if    order is passerformes and
        wings is long_pointed and
        tail is forked and
        bill is short 
  then  family is swallow cf 80.

rule 13
  if    family is albatross and
        color is white 
  then  bird is laysan_albatross cf 80.

rule 14
  if    family is albatross and
        color is dark 
  then  bird is black_footed_albatross cf 80.

rule 15
  if    order is tubenose and
        size is medium and
        flight is flap_glide 
  then  bird is fulmar cf 80.

rule 16
  if    family is swan and
        voice is muffled_musical_whistle 
  then  bird is whistling_swan cf 80.

rule 17
  if    family is swan and
        voice is loud_trumpeting 
  then  bird is trumpeter_swan cf 80.

rule 18
  if    family is goose and
        season is winter and
        country is united_states and
        head is black and
        cheek is white 
  then  bird is canada_goose cf 80.

rule 19
  if    family is goose and
        season is summer and
        country is canada and
        head is black and
        cheek is white 
  then  bird is canada_goose cf 80.

rule 20
  if    family is goose and
        color is white 
  then  bird is snow_goose cf 80.

rule 21
  if    family is duck and
        voice is quack and
        head is green 
  then  bird is mallard cf 80.

rule 22
  if    family is duck and
        voice is quack and
        color is mottled_brown 
  then  bird is mallard cf 80.

rule 23
  if    family is duck and
        voice is short_whistle 
  then  bird is pintail cf 80.

rule 24
  if    family is vulture and
        flight_profile is v_shaped 
  then  bird is turkey_vulture cf 80.

rule 25
  if    family is vulture and
        flight_profile is flat 
  then  bird is california_condor cf 80.

rule 26
  if    family is falcon and
        eats is insects 
  then  bird is sparrow_hawk cf 80.

rule 27
  if    family is falcon and
        eats is birds 
  then  bird is peregrine_falcon cf 80.

rule 28
  if    family is flycatcher and
        tail is long_rusty 
  then  bird is great_crested_flycatcher cf 80.

rule 29
  if    family is flycatcher and
        throat is white 
  then  bird is ash_throated_flycatcher cf 80.

rule 30
  if    family is swallow and
        tail is forked 
  then  bird is barn_swallow cf 80.

rule 31
  if    family is swallow and
        tail is square 
  then  bird is cliff_swallow cf 80.

rule 32
  if    family is swallow and
        color is dark 
  then  bird is purple_martin cf 80.

rule 33
  if    region is new_england 
  then  country is united_states.

rule 34
  if    region is south_east 
  then  country is united_states.

rule 35
  if    region is mid_west 
  then  country is united_states.

rule 36
  if    region is south_west 
  then  country is united_states.

rule 37
  if    region is north_west 
  then  country is united_states.

rule 38
  if    region is mid_atlantic 
  then  country is united_states.

rule 39
  if    region is ontario 
  then  country is canada.

rule 40
  if    region is quebec 
  then  country is canada.


  
ask=bill,
  'What type of bill?'=[hooked,flat,sharp_hooked,short,other].

ask=cheek,
  'What type of cheek?'= [white,other].

ask=color,
  'What color is it?'= [white,dark,mottled_brown,other].
  
ask=region,
'What region was it seen in?' = [
   new_england, south_east, mid_west, south_west,
	 north_west, mid_atlantic, ontario, quebec, other].

ask=eats,
  'What does it eat?'= [
     meat, flying_insects, insects, birds, other].

ask=feed,
  'Where does it feed?' = [
     on_water_surface, scavange, other]. 

ask=feet,
  'What type of feet?' =	[webbed, curved_talons, one_long_backward_toe, other].

ask=flight,
'What type of flight?'= [ponderous,powerful,agile,flap_glide,other].

ask=flight_profile,
'What is the flight profile?'=[v_shaped,flat,other].

ask=head,
  'What type of head?'=[large ,black, green, other].

ask=live,
  'Where does it live?' = [at_sea,other].

ask=neck,
  'What type of neck does it have?' = [long,other].

ask=nostrils,
  'What type of nostrils?'=	[external_tubular,other].

ask=season,
  'What season was it seen in?'= [summer, fall, winter, spring].

ask=size,
'What size is it?'=	[large, medium, small, plump, other].

ask=tail,
  'What type of tail?'=	[narrow_at_tip, forked, long_rusty, square, other].

ask=throat,
  'What type of throat?'=	[white, other].

ask=voice,
 'What type of voice?'=	[muffled_musical_whistle, 
 loud_trumpeting, quack, short_whistle, other].

ask=wings,
  'What type of wings does it have?'=	[long_narrow, 
     broad, long_pointed, other].