"""
ok : a simple python unit test engine 
Copyright (c) 2015, Tim.Menzies@gmail.com. 
Licenses under the WTFPL http://www.wtfpl.net/

Inspired by Kent Beck's video 
https://www.youtube.com/watch?v=nIonZ6-4nuU.

For example usage, see the _ok function (at end)
"""

##-- top-level driver - ----------------------------

class u:
  tries = fails = 0  #  tracks the record so far
  report= "# TRIES= %s FAIL= %s TEST= %s : %s" 
  @staticmethod
  def ok(*lst):
    for one in items(lst): u(one)
    return one
  def __init__(i,test):
    u.tries += 1
    try:
      test()
    except Exception,e:
      u.fails += 1
      print u.report % (
            u.tries,u.fails,test.__name__,e)
  

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
@u.ok # how to always run+test something at load time
def noop():
  "Never fails"
  return True

@u.ok # how to always run+test something at load time
def oops():
  "Always fails"
  5/0

def _ok():
  "Test the test engine"
  u.ok(oops,noop,
     lambda: 1+1,lambda: 4/0)
  assert u.tries == 6
  assert u.fails == 3

#---| maybe, test the test engine |---------------
if __name__ == '__main__':
  _ok(); print "Success!!!"
