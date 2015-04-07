from __future__ import division
from lib import *
from n   import *

@setting
def MODEL(**d): return o(
  num    = "$",
  missing= "?",
  less   = "<"
  ).add(**d)

class Model: 
  def score(i,_): return 0
  def ok(i,_):    return True
  def has(i):     return o(x=[], y=[])
  def __init__(i):
    i.xNums, i.xSyms= [],[]
    i.yNums, i.ySyms= [],[]
    i.x,     i.y    = [],[]
    tmp = i.has() 
    i.x = i.spec(tmp.x, i.xNums, i.xSyms)
    i.y = i.spec(tmp.y, i.yNums, i.ySyms)
  def spec(i, lst, nums, syms):
    nump=lambda x: the.MODEL.num in x.name
    for x in lst:
      x.like = the.MODEL.less not in x.name
      where    = nums if nump(x) else syms
      where   += [x]
    return lst