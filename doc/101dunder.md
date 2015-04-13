[<img width=900 src="https://raw.githubusercontent.com/timm/15/master/src/img/banner.jpg">](https://github.com/timm/15/blob/master/README.md)

_Go to: [Home](https://github.com/timm/15/blob/master/README.md) | [Sitemap](https://github.com/timm/15/blob/master/TOC.md)_


# 101dunder.py


 q   +-----+  r  +-----+
---->|  C  |---->|  D  |--> s
 ^   +-----+     +-+---+
 |                 |
 +-----------------+ 

C = stock of clean diapers
D = stock of dirty diapers
q = inflow of clean diapers
r = flow of clean diapers to dirty diapers
s = out-flow of dirty diapers

````python
def sim(state0,life=100,spy=False):
  for t in xrange(life):
    if spy:
      print t,state0
    state1 = state0.copy()
    yield t,state0,state1
    for key in state1.content():
      if state1[key]  < 0:
        state1[key] = 0
    state0 = state1
  
def diapers():
  state0 = o(C=20, D=0, q=0, r=8, s=0)
  for t,u,v in sim(state0,60,spy=True):
    v.C = u.C + u.q - u.r
    v.D = u.D + u.r - u.s
    v.q = 70 if t % 7 == 6 else 0 
    v.s = u.D if (t % 7 == 6) else 0
    if t == 34: # special case (the day i forget)
      v.s = 0
  print t,u


diapers()
````

__________

<img width=200 align=right src="https://raw.githubusercontent.com/timm/15/master/src/img/wtfpl.png">
Copyright © 2015 Tim Menzies <tim.menzies@gmail.com>.

This work is free. You can redistribute it and/or modify it under the
terms of the Do What The F*ck You Want To Public License, Version 2,
as published by Sam Hocevar. See [here](http://www.wtfpl.net/faq/) for more details.
