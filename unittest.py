"""
ok : a simple python unit test engine 
Copyright (c) 2015, Tim.Menzies@gmail.com. 
Licenses under the WTFPL http://www.wtfpl.net/

Inspired by Kent Beck's video 
https://www.youtube.com/watch?v=nIonZ6-4nuU.

For example usage, see the _ok function (at end)
"""

##-- top-level drivers ----------------------------
def ok(*f):
  """convenience function for unittests and 
   running+testing code at load time."""
  unittest(f);
  return f[0] if listp(f) else f
    
class unittest:
  "The worker."
  tries = fails = 0  #  tracks the record so far
  def __init__(i,*tests):
    for test in items(tests):
      unittest.tries += 1
      try:
        test()
      except Exception,e:
        unittest.fails += 1
        print "# TRIES= %s FAIL= %s %s" % (
              unittest.tries, unittest.fails,
              "TEST= %s : %s" % (test.__name__,e))


#---| misc support code |--------------------------
def listp(x):
  return isinstance(x,(list,tuple))

def items(x):  
  """Convenience iterator. Recursively returns all
      non-list items within nested lists."""
  if listp(x):
    for y in x:
      for z in items(y):
        yield z
  else:
    yield x

#---| example calls |------------------------------
@ok # how to always run+test something at load time
def noop():
  "Never fails"
  return True

@ok # how to always run+test something at load time
def oops():
  "Always fails"
  5/0

def _ok():
  "Test the test engine"
  ok(oops,noop,
     lambda: 1+1,lambda: 4/0)
  assert unittest.tries == 6
  assert unittest.fails == 3

#---| maybe, test the test engine |---------------
if __name__ == '__main__':
  _ok(); print "Success!!!"
