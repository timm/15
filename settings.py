"""
Settings idioms
#1) stored in 1 global place (easier to mutate)
#2) have defaults, which can be overridden
#3) when overridden, can be reset to defaults
    by calling some function
"""

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

@setting # example of setting
def STUDY(**d): return o(
    seed    =   1,
    repeats = 100
    ).add(**d)

@contextmanager
def settings(f,**d):
  "# 3) can be set, then reset to zero"
  yield f(**d)
  f()

@contextmanager
def study(seed=None):
  "Standard idioms around a study."
  random.seed(seed or the.STUDY.seed)
  show = datetime.datetime.now().strftime
  print("\n#" + "-" * 50)
  print("#", show("%Y-%m-%d %H:%M:%S"))
  t1 = time.time()
  print(the,"\n")
  yield None
  t2 = time.time() # show how long it took to run
  print("\n" + "-" * 72)
  print("# Runtime: %.3f secs" % (t2-t1))
