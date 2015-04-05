from lib import *


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
