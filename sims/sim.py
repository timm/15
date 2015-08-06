from __future__ import division

import random
r = random.random
any = random.choice

def ps(dims,bins,p=0.1,skew=2):
  space = bins**dims
  f1  = [r()**skew for _ in xrange(space)]
  all = sum(f1)
  f2  = [x/all for x in f1]
  return [p*1/space*x for x in f2]

def ns(dims=3,bins=2,p=0.1):
  w = sum(ps(dims,bins,p))
  n = 10
  found = 0
  while found < 0.66 and n < 1000:
    n += 10
    found = 1 - ((1 - w) ** n)
  print "_%s, _%s, _%s, %s" % (int(p*10),dims,bins,n)

print "p,dims,bins,n66"
for _ in xrange(1000):
  ns(dims= any([3,4,5,6,7]),
     bins= any([2,3,4,5,6,7]),
     p   = any([0.1,0.2,0.3,0.4]))

"""
bins =  _2
|   dims =  _3 : 50 (25/672) [11/436.36]
|   dims =  _4 : 107.6 (20/3028.75) [5/3456.25]
|   dims =  _5 : 203.26 (31/11974.82) [12/10088.09]
|   dims =  _6 : 336.43 (17/31955.71) [11/31618.62]
|   dims =  _7 : 613.33 (23/64163.71) [7/87900.89]
bins =  _3
|   dims =  _3 : 159.14 (21/7091.16) [14/8226.53]
|   dims =  _4 : 455.48 (22/58697.52) [9/107415.61]
|   dims =  _5 : 905.79 (24/17515.97) [14/14086.41]
|   dims =  _6 : 1000 (18/0) [18/0]
|   dims =  _7 : 1000 (17/0) [7/0]
bins =  _4
|   dims =  _3 : 370 (19/27314.13) [8/51881.93]
|   dims =  _4 : 891.94 (22/16804.96) [9/19220.29]
|   dims =  _5 : 1000 (33/0) [11/0]
|   dims =  _6 : 1000 (16/0) [18/0]
|   dims =  _7 : 1000 (30/0) [18/0]
bins =  _5
|   dims =  _3 : 755.31 (20/61678.75) [12/72781.25]
|   dims =  _4 : 1000 (23/0) [17/0]
|   dims =  _5 : 1000 (22/0) [12/0]
|   dims =  _6 : 1000 (18/0) [12/0]
|   dims =  _7 : 1000 (20/0) [14/0]
bins =  _6
|   dims =  _3 : 860 (18/28511.11) [9/28511.11]
|   dims =  _4 : 1000 (18/0) [5/0]
|   dims =  _5 : 1000 (19/0) [5/0]
|   dims =  _6 : 1000 (29/0) [15/0]
|   dims =  _7 : 1000 (25/0) [9/0]
bins =  _7 : 998.33 (116/41.88) [52/278.18]

corelation:  0.9178

"""
    
