from __future__ import print_function,division

class o:
  def __init__(i,**d)    : i.add(**d)
  def d(i)               : return i.__dict__
  def add(i,**d)         : i.d().update(d);return i
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __getitem__(i,k)   : return i.__dict__[k] 

the = o()

def settings(f):
  name = f.__name__
  def wrapper(**d):
    tmp = the[name] = f().add(**d)
    return tmp
  wrapper()
  return wrapper

def ok(*lst):
  for one in lst: unittest(one)
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
    print("# TRIES= %s FAIL= %s TEST= %s : %s"  % (
          unittest.tries, unittest.fails,
          test.__name__, e))
    
