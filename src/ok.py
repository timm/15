# ok.py : a simple test engine

# BEFORE reading this, get inspired. View Kent 
# Beck's great video : 
# https://www.youtube.com/watch?v=nIonZ6-4nuU."""

# AFTER reading this, look at okok.py for examples
# on how to use this.

# And AFTER reading that, everyime you write a 
# file x.py, add in some tests to xok.py.

# Get a better print function 
from __future__ import print_function

# Syntatic sugar.
def ok(*lst):
  """Calls the test engine. Also, can be used
     to call and test code at load time."""
  for one in lst: unittest(one)
  return one
  
class unittest:
  """"Farcade for storing tries/fails counts
      and the test engine."""
  tries = fails = 0  #  tracks the record so far
  def __init__(i,test):
    unittest.tries += 1
    try:
      test()
    except Exception,e:
      unittest.fails += 1
      i.report(e,test)
  def report(i,e,test):
    print("# TRIES= %s FAIL= %s TEST= %s : %s"  % (
          unittest.tries, unittest.fails,
          test.__name__, e))
