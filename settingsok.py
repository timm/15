from __future__ import division,print_function
from settings import *
from unittest import *
import random

# example of how to write a setting function
@setting
def DEMO(**d): return o(
    mu=0,
    seed=1,
    sd=2,
    repeats=32
  ).add(**d)

@ok
def settingsok():
  assert the.DEMO.mu == 0
  with settings(DEMO, mu=2, repeats=128):
    with study(seed= 10):
      assert the.DEMO.mu == 2
      n   = the.DEMO.repeats
      tmp = [random.gauss(the.DEMO.mu,
                           the.DEMO.sd)
             for _ in xrange(n)]
      print('RESULTS:',
            o(n= n, mu= sum(tmp)/n))
  assert the.DEMO.mu == 0
