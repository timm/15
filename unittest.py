from __future__ import print_function

def ok(*lst):
  for one in lst: unittest(one)
  return one
  
class unittest:
  """Inspired by Kent Beck's video 
  https://www.youtube.com/watch?v=nIonZ6-4nuU."""
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
