[<img width=900 src="https://raw.githubusercontent.com/timm/15/master/src/img/banner.jpg">](https://github.com/timm/15/blob/master/README.md)

_Go to: [Home](https://github.com/timm/15/blob/master/README.md) | [Sitemap](https://github.com/timm/15/blob/master/TOC.md)_


# settings.py

Settings idioms
#1) stored in 1 global place (easier to mutate)
#2) source code for making settings can be spread
    all over the code
#3) settings have defaults, which can be overridden
#4) when overridden, can be reset to defaults
    by calling some function
````python

from __future__ import print_function,division
from contextlib import contextmanager
from o import *
import random, datetime, time

the=o() #1) idioms stored in global place

def setting(f):
  "#2) have defaults which can overridden."
  def wrapper(**d):
    tmp = the[f.__name__] = f().add(**d)
    return tmp
  wrapper()
  return wrapper

#2) i can write multiple settings functions X,Y,Z
#   anywhere in the code; and these can be accessed
#   via the.X and the.Y and the.Z;
#3) and can be reset  to their redefaults by X(), Y(), Z();
#4) these can be adjusted via e.g. STUDY(seed=2).

@setting 
def STUDY(**d): return o(
    seed    =   1,
    repeats = 100
    ).add(**d)

@contextmanager
def settings(f,**d):
  "First, tweak the settings. Then, reset to default."
  yield f(**d)
  f()

def use(x,**y): return (x,y)

@contextmanager
def study(what,*usings):
  """Standard idioms around a study.
  1) BEFORE
     1a) Print what the run is about.
     1b) report date and time of run
     1c) before run, make some special setings
     1d) Set the random number seed.
     1e) Print the settings used in this run.
  2) AFTER
     2a) show total runtime
     2b) reset settings to defaults"""
  # 1) BEFORE
  print("\n#" + "-" * 50)
  print("#",what)                         #1a 
  show = datetime.datetime.now().strftime
  print("#", show("%Y-%m-%d %H:%M:%S"))   #1b
  t1 = time.time()
  for (using, override) in usings:  
    using(**override)                     #1c
  rseed(the.STUDY.rseed)                  #1d
  print(the,"\n")                         #1e
  yield
  # 2) AFTER
  t2 = time.time() # show how long it took to run
  print("\n" + "-" * 72)
  print("# Runtime: %.3f secs" % (t2-t1)) #2a
  for (using,_) in usings:
    using()                               #2b
````

__________

<img width=200 align=right src="https://raw.githubusercontent.com/timm/15/master/src/img/wtfpl.png">
Copyright © 2015 Tim Menzies <tim.menzies@gmail.com>.

This work is free. You can redistribute it and/or modify it under the
terms of the Do What The F*ck You Want To Public License, Version 2,
as published by Sam Hocevar. See [here](http://www.wtfpl.net/faq/) for more details.
