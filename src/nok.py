from __future__ import division,print_function
from lib import *
from n   import *

@ok
def _nok():
  r1 = range(10)
  r2 = range(10,20)
  n1 = N(r1)
  n2 = N(r1+r2)
  assert nearly(n1.sd(), 3.0277), "wrong sd"
  assert nearly(n1.mu,   4.5),    "wrong mu"
  for x in r2:
    n2 -= x
  assert nearly(n1.mu,   n2.mu),    "bad mu"
  assert nearly(n1.sd(), n2.sd()),  "bad sd"

@ok
def _cliffsDelta():
  lst0 = [r() for _ in xrange(1000)]
  f = 1.025
  for n in range(10):
    f = f**1.5
    lst1 = [x*f for x in lst0]
    expect = False if f < 1.2 else True
    assert expect == cliffsDelta(lst0, lst1)
