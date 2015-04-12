from __future__ import division,print_function
from settings import *
from unittest import *
import random

# example of how to write a setting function
@setting
def DEMO(**d): return o(
    mu=0,
    sd=2,
    repeats=32
  ).add(**d)

@setting
def COLOR(**d): return o(
  back='green',
  front='red'
  ).add(**d)

@ok
def settingsok():
  assert the.DEMO.mu     == 0
  assert the.COLOR.front == 'red'
  with study("big purple people eaters",
           use(DEMO, mu=2, repeats=1000000),
           use(COLOR,front='purple'),
           use(STUDY,seed=10)):
    assert the.DEMO.mu == 2
    assert the.COLOR.front == 'purple'
    n   = the.DEMO.repeats
    tmp = [random.gauss(the.DEMO.mu,
                      the.DEMO.sd)
           for _ in xrange(n)]
    print('RESULTS:',
        dict(seed= the.STUDY.seed,
             n   = n,
             mu  = sum(tmp)/n))
  assert the.DEMO.mu     == 0
  assert the.COLOR.front == 'red'

"""
#--------------------------------------------------
# big purple people eaters
# 2015-04-05 08:04:28
{ 'COLOR': { 'back': 'green', 'front': 'purple'},
  'DEMO': { 'mu': 2, 'repeats': 1000000, 'sd': 2},
  'STUDY': { 'repeats': 100, 'seed': 10}} 

RESULTS: {'mu': 1.9982820946390811, 'seed': 10, 'n': 1000000}

------------------------------------------------------------------------
# Runtime: 4.819 secs
"""
