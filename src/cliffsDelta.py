from __future__ import division
from lib import *

def cliffsDelta(lst1,lst2,dull=None):
  def runs(lst):
    "Reduce runs of repeats to count,item."
    for j,two in enumerate(lst):
      if j == 0:
        one,i = two,0
      if one!=two:
        yield j - i,one
        i = j
      one = two
    yield j - i + 1,two
  dull = dull or the.N.dull
  m, n = len(lst1), len(lst2)
  lst2 = sorted(lst2)
  j = more = less = 0
  for repeats,x in runs(sorted(lst1)):
    while j <= (n - 1) and lst2[j] <  x: 
      j += 1
    more += j*repeats
    while j <= (n - 1) and lst2[j] == x: 
      j += 1
    less += (n - j)*repeats
  d= (more - less) / (m*n + 0.000001) 
  return abs(d)  > dull
