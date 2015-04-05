from unittest import *

#---| example calls |------------------------------
# how to always run+test something at load time
@ok
def noop(): return True
 
@ok 
def oops(): 5/0

def _ok():
  ok(oops,noop,lambda: 1+1,lambda: 4/0)
  ok(oops)
  ok([oops,noop])
  assert unittest.tries == 10
  assert unittest.fails == 5

_ok()
