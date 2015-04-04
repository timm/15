from __future__ import division,print_function

from unittest import *

def isa(x,y):
  return isinstance(x,y)
    
def showHas(x):
  import pprint
  pprint.pformat([x for x in has(x)])
