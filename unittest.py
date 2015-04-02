"""
ok : a simple python unit test engine 
Copyright (c) 2015, Tim.Menzies@gmail.com. 
Licenses under the WTFPL http://www.wtfpl.net/

Inspired by Kent Beck's video 
https://www.youtube.com/watch?v=nIonZ6-4nuU.

For example usage, see the _ok function (at end)
"""

##-- top-level driver - ----------------------------
def ok(*lst):
  for one in items(lst):
    unittest(one)
  return one
  
class unittest:
  tries = fails = 0  #  tracks the record so far
  def __init__(i,test):
    unittest.tries += 1
    try:
      test()
    except Exception,e:
      unittest.fails += 1
      i.report(e,test)
  def report(i,e,test):
    print "# TRIES= %s FAIL= %s TEST= %s : %s"  % (
          unittest.tries, unittest.fails,
          test.__name__, e)

#---| misc support code |--------------------------
def items(x):  
  "Recursively yield non-list items in nested list"
  def listp(x): return isinstance(x,(list,tuple))
  if listp(x):
    for y in x:
      for z in items(y):
        yield z
  else:
    yield x

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
  assert unittest.tries == 9
  assert unittest.fails == 5

#---| maybe, test the test engine |---------------
if __name__ == '__main__':
  _ok()
  print "Success!!!"
