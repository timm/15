# okok.py
# Examples of using unittests

from ok import * # get the test eingine

# eg1:  run+test something at load time
@ok
def noop(): return True # never fails
 
# eg2:  ditto
@ok 
def oops(): 1/0  # always fails

# eg3: test the test engine
@ok
def unittestok():
  ok(oops,       # "ok" accepts multiple arguments
    noop,        # can be named functions
    lambda: 1+1, # or anonymous functions
    lambda: 1/0
    )
  ok(oops)       # ok can also run with 1 test
  ok(oops,noop)  
  # note that, when runm we never see 'unitest fail'
  assert unittest.tries == 10, 'unit test fail'
  assert unittest.fails == 5,  'unit test fail'
  

