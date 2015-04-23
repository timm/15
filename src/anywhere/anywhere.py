from __future__ import print_function,division

from lib import *

  

                    
#------------------------------------------------    
def norm(i,r):
  return (i - r.lo) / (r.hi - r.lo + 0.00001)

def trim(n,r):
  return max(r.lo, min(n, r.hi))

def dist(cells1,cells2,t, skip="?"):
  n = inc = 0
  for col in t.indep:
    x = cells1[col]
    y = cells2[col]
    if x==skip and y==skip:
      continue
    n += 1
    if col in t.sym:
      inc  += 0 if x==y else 1
    else:
      if x != skip: x= norm(x,t.num[col])
      if y != skip: y= norm(y,t.num[col])
      if x == skip: x= 1 if y<0.5 else 0
      if y == skip: y= 1 if x<0.5 else 0
      inc  += (x-y)**2
  return inc**0.5 / n**0.5

#------------------------------------------------    

