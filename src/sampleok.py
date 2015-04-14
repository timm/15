from __future__ import division,print_function
from sample import *

@ok
def sample0ok():
  rseed(1)
  some=Numbers(size=32)
  for x in xrange(1000):
    some += x
  print(some.all())
  
@ok
def sample1ok():
  rseed(1)
  lst  = [r() for _ in xrange(1000)]
  some = Numbers(lst)
  print(ntiles(gs(sorted(lst))))
  print(ntiles(gs(some.all())))
  
@ok
def sample2ok():
  """How different are the deltas between
     two random samples, keeping all nums
     or just a small sample."""
  def delta(lst1,lst2):
    sum, diff = 0, 0
    for x,y in zip(sorted(lst1),
                   sorted(lst2)):
      sum  += x
      diff += x - y
    return int(100*diff/sum)
  rseed(1)
  for m in [32,128,512,2048,8196,32784]:  
    print(":samples %g"% m,end=" ")
    for n in [32, 64,128,256,512]:
      all1, all2 = [],[]
      c1 = Numbers(size=n)
      c2 = Numbers(size=n)
      for _ in xrange(m):
        x,y = r(), r()
        c1 += x
        c2 += y
        all1 += [x]
        all2 += [y]
      sub1 = c1.all()
      sub2 = c2.all()
      print(":size %g"% n,
            ":sub %g" % delta(sub1, sub2),
            ":all %g" % delta(all1, all2),
            end=" ")
    print("")

@ok
def numbersOk():
  rseed(1)
  n    = 1024
  lst1 = [r() for _ in xrange(n)]
  m    = 1.005
  for _ in xrange(10):
    m = m**2
    lst2 = map(lambda x : x*m, lst1)
    print(m, Numbers(lst1) != Numbers(lst2))




