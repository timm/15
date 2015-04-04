from __future__ import division,print_function
sys.dont_write_bytecode = True

from lib import *

class o:
  def __init__(i,**d): i.add(**d)
  def __iadd__(i,**d) : i.__dict__.update(**d); return i
  def has(i):
    return {k:has(v) for k,v in i.__dict__}
  def __repr__(i)   :
    return showHas(i)
    

print(o(name=21,
        wiehgt=o(aa=2,bb=3)))
      
