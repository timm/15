<img width=900 src="https://raw.githubusercontent.com/timm/15/master/src/img/banner.jpg">

_Go to: <a href="https://raw.githubusercontent.com/timm/15/master/README.md">Home</a> | <a href="https://raw.githubusercontent.com/timm/15/master/TOC.md">TOC</a>




# Timm's Search-based Tools (in Python)

["_There are some who call me... Tim?_"](https://www.youtube.com/watch?v=JTbrIo1p-So)

## Under Construction

This site will be a "howto" guide on combine SBSE and data mining tools
to explore models. Right now, its much less than that. But it will be the
toolkit used for the Fall 2015 graduate subject _Automated
(Model-Based) Software Engineering_.
Share and enjoy... but not quite yet.

## Contents

This site contains numerous [links to example models](doc/examplemodels.md). 

As to the rest, it comprimises:

+ 10% **intro Python** examples;
+ 20% **theory** of model-based and search-based SE;
+ 20% how to **build** models (using Python DSLs, using raw programming, uses interfaces to other systems);
+ 30% how to **search** models (multi-objective optimization, plus some data mining);
+ 20% how to **watch** model output (experimental methods to understanding models).

## Anything Here that is Special and Different? 

One big emphasis in my work is the comparative analysis of different approaches:

+ It seems
   to me that you can't just describe (say) two optimization algorithms-- you also have to
   provide the machinery that can assess which of these algorithms works best on different problems.
+ Hence,  much of this code concerns the rig _around_ the algorithms that watches and assesses
   their performance.

Also, there  is stong connection between  data mining can  optimization:

+ While this theoetical
  connection  is widely acknowledged, I am unaware of work takes the next step to 
  to combine/ clarify/ simplify these two approaches. 
+ My suspicions are that both approaches
   are really combinations of a lower-level set of primitive operators.
+ The   goal of this work is to indentify those operators, and offer sample implementations.
+ Watch this space!

## Before you start  

Time to freshen your Python skills:

+ Do you understand my [intro Python examples](doc/101python.md)? 
+ Note that some of the techniques in the intro are reused (extensively) in the rest of this code base.
 
