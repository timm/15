from __future__ import division,print_function
from lib   import *
from cache import *


def cacheok():
  def delta(lst1,lst2):
    sum, diff = 0, 0
    for x,y in zip(sorted(lst1),sorted(lst2)):
      sum  += x
      diff += x - y
    return int(100*diff/sum)
  rseed(1)
  for m in [32,64,128,256,512,1024]:
    print("")
    for n in [64,128,256,512]:
      all1, all2 = [],[]
      c1 = SortedCache(size=n)
      c2 = SortedCache(size=n)
      for _ in xrange(m):
        x,y = r(), r()
        c1 += x
        c2 += y
        all1 += [x]
        all2 += [y]
      print(m,n,
            delta(c1.cached(), c2.cached()),
            delta(all1, all2))

cacheok()
