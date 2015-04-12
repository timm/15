from __future__ import division,print_function
from lib import *
from cache import *x
from n   import *

# should define better in each goal

@setting
def WATCH(**d): return o(
    trivial = 0.01,
    tiles   = [0.1, 0.3, 0.5, 0.7, 0.9 ],
    maxEvals=10000
    lives   = 5
    ).add(**d)

def ntiles(lst,tiles):
  thing = lambda z: lst[ int(len(lst)*z)  ]
  return [ thing(tile) for tile in tiles ]

class Watch:
  def __init__(i):
    i.evals = the.WATCH.maxEvals
    i.last,  i.best= None,None
    i.all = Cache()
    i.history = []
    i.rank, i.pool = 0, []
    i.lives        = the.WATCH.lives
  def middle(lst):
    lst = sorted(lst)
    return lst, lst[ int(len(lst)/2) ]
  def improvement(i,now,last):
    if last and now:
      if cliffsDelta(now.has,last.has):
        if abs(m0 - m1)/m0 > the.WATCH.trivial:
          if better(m0,m1):
            return True
      return False
    else:
      return True
  def another(i,pop, score=last,better=gt):
    i.evals -= len(pop)
    pop,mid = i.middle(pop)
    pop = o(has = pop,
            mid = mid,
            rank= 1,
            titles= ntiles(pop,the.WATCH.tiles))
    i.history += [pop]
    if improvement(pop,pool):
      i.lives += 1  
      i.rank  += 1
      i.pool   = pop
      if improvement(i.best,pop):
        i.best = pop
    else:
      i.lives -= 1
      i.pool  += pop
    pop.rank = i.rank
    return lives > 0 and i.evals > 0
    
