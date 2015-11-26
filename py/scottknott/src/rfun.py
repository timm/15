from rclass import *

def rc(data) :  
  return r(data,RC(data))

def r(data,control):
  def recurse(bags,all,rank=1) :
    "recurse on good splits of 'lst', if they exists"
    cut,left,right = split(bags,all)
    if not cut:
      for x in bags: x.rank = rank
    else:
      rank = recurse(bags[:cut],left,rank) + 1
      rank = recurse(bags[cut:],right,rank)
    return rank
  def split(bags,all):
    "find  best cut of 'bags' into 'lhs' and 'rhs'"
    before, lhs = control.now0(), bags[0]
    cut, now, left, right = None, None,None,None
    for i,one in enumerate(bags):
      if i==0: continue
      rhs = all - lhs
      now = control.now(all,lhs,rhs)
      if control.better(before,now):
        if control.different(lhs,rhs) :
          before,cut,left,right = now,i,lhs,rhs
      lhs += one
    return cut,left,right
  bags = sorted(data)
  all  = reduce(lambda x,y: x+y, bags)
  recurse(bags,all)
  for bag in sorted(bags): print bag
