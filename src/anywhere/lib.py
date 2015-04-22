from __future__ import print_function,division
import random, pprint, re, datetime, time
from contextlib import contextmanager
import pprint
from boot import *

@settings
def LIB(): return o(
    seed =  1,
    has   = o(decs = 3,
              skip="_",
              wicked=True),
    show  = o(indent=2,
              width=80)
)
#-------------------------------------------------
isa   = isinstance
fun   = lambda x:x.__class__.__name__ == 'function'
r     = random.random
any   = random.choice
seed = random.seed

def shuffle(lst):
  random.shuffle(lst)
  return lst

def show(x, indent=None, width=None):  
  print(pprint.pformat(has(x),
            indent= indent or the.LIB.show.indent,
            width = width  or the.LIB.show.width))

def has(x,  decs=None, wicked=None, skip=None) :
  if decs   is None:
    decs   = the.LIB.has.decs
  if wicked is None:
    wicked = the.LIB.has.wicked
  if skip   is None:
    skip   = the.LIB.has.skip
  if   isa(x, o):
    return has({'o': x.d()})
  elif isa(x,list):
    return map(has,x)
  elif isa(x,float):
    return round(x,decs)
  elif fun(x):
    return x.__name__+'()'
  elif wicked and hasattr(x,"__dict__"):
      return has({x.__class__.__name__ : x.__dict__})
  elif isa(x, dict):
    return {k:has(v)
            for k,v in x.items()
            if skip != k[0]}
  else:
    return x

@contextmanager
def duration(n=1):
  t1 = time.time()
  yield
  t2 = time.time()
  print("\n" + "-" * 72)
  print("# Runtime: %.3f secs" % ((t2-t1)/n))

def use(x,**y): return (x,y)

@contextmanager
def study(what,*usings):
  print("\n#" + "-" * 50,
        "\n#", what, "\n#",
        datetime.datetime.now().strftime(
          "%Y-%m-%d %H:%M:%S"))    
  for (using, override) in usings:
    using(**override)              
  seed(the.LIB.seed)            
  show(the)                   
  with duration():
    yield
  for (using,_) in usings:
    using()               
