"""
Settings idioms
1) stored in one place (easier to mutate)
2) have defaults, which can be overridden
3) when overridden, can be reset to defaults
    by calling some function
"""

from __future__ import print_function,division
from contextlib import contextmanager
from o import *
import random, datetime, time

the=o() # idioms stored in place

def setting(f):
  "Settings can be overridden and reset."
  def wrapper(**d):
    tmp = the[f.__name__] = f().add(**d)
    return tmp
  wrapper()
  return wrapper

@setting # example of making a setting function
def STUDY(**d): return o(
    seed    =   1,
    repeats = 100
    ).add(**d)

@contextmanager
def settings(f,**d):
  "Change some settings, then reset to defaults."
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
