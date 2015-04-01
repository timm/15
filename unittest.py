"""
ok : a simple python unit test engine 
Copyright (c) 2015, Tim.Menzies@gmail.com. 
Licenses under the WTFPL http://www.wtfpl.net/

Inspired by Kent Beck's video 
https://www.youtube.com/watch?v=nIonZ6-4nuU.

For example usage, see the _ok function (at end)
"""

def items(x):  
  """Convenience iterator. Recursively returns all
      non-list items within nested lists."""
  if isinstance(x,(list,tuple)):
    for y in x:
      for z in items(y):
        yield z
  else:
    yield x
    
class ok:
  tries = fails = 0  #  tracks the record so far
  def __init__(i,*tests):
    for test in items(tests):
      ok.tries += 1
      try:
        test()
      except Exception,e:
        ok.fails += 1
        print "# TRIES= %s FAIL= %s %s" % (
              ok.tries, ok.fails,
              "TEST= %s : %s" % (test.__name__,e))
        
def noop():
  "Never fails"
  return True
def oops():
  "Always fails"
  5/0

def _ok():
  "Test the test engine"
  ok(oops,noop,
     lambda: 1+1,lambda: 4/0)
  assert ok.tries == 4
  assert ok.fails == 2

if __name__ == '__main__':
  _ok(); print "Success!!!"
