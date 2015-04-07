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
  
class Schaffer(Model): 
  def has(i):
    return o(x=[N(name="$x1",lo=-10,hi=10)],
             y=[N(name="<f1"),
                N(name="<f2")])
  def score(i,row):
    x = row[0]
    return [x*2, (x-2)**2]
    
class Kursawe(Model): 
  def has(i):
    return o(x=[Num(name="$x1",lo = -5,hi = 5),
                Num(name="$x2",lo = -5,hi = 5),
                Num(name="$x3",lo = -5,hi = 5),
                Num(name="$x4",lo = -5,hi = 5),
                Num(name="$x5",lo = -5,hi = 5),
                Num(name="$x6",lo = -5,hi = 5),
                Num(name="$x7",lo = -5,hi = 5),
                Num(name="$x8",lo = -5,hi = 5)],
             y=[Num(name="<f1"),
                Num(name="<f2")])
  def score(i,row):
    f1 = f2 = 0
    for n,one in enumerate(row[:7]):
      two = row[n+1]
      f1 += -10*e**(-0.2*(one**2 + two**2)**0.5)
    for one in row[:8]:
      f2 += abs(one)**0.8 + 5*sin(one**3)
    return [f1, f2]