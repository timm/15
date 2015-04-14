from __future__ import division,print_function
from lib import *

@setting
def SAMPLE(): return o(
  cache = 128,
  dull  = [0.147, # small
           0.33,  # medium
           0.474  # large
          ][0]
  )

class Sample:
  "Keep, at most, 'size' things."
  def __init__(i, init=[], size=None):
    i.max = size or my.SAMPLE.cache
    i.n, i.all, i.ordered = 0, [], False
    map(i.__iadd__,init)
  def __iadd__(i,x):
    i.ordered = False
    i.n += 1
    now  = len(i.all)
    if now < i.max:
      i.all += [x]
    elif r() <= now/i.n:
      i.all[ int(r() * now) ]= x
    return i

class Numbers:
  "Keep, at most, 'size' numbers, in sorted order."
  def __init__(i,init=[],size=None):
    i._cache =  Sample(init,size)
    i.sorted = False
  def __iadd__(i,x):
    i._cache += x
    i.sorted  = False
    return i
  def all(i):
    if not i.sorted:
      i._cache.all = sorted(i._cache.all)
    i.sorted = False
    return i._cache.all
  def __repr__(i):
    return '<'+str(i._cache.all)+'>'
  def __ne__(i,j):
    gt = lt = n = 0
    for one in i.all():
      for two in j.all():
        n += 1
        if one > two: gt += 1
        if one < two: lt += 1
    return abs(gt - lt)/n > my.SAMPLE.dull
    
 
