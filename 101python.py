from __future__ import print_function,division
from uniitest import *
import math

class yourFirstClass:
  "init is called when created)
  def __init__(i,x) : i.mine = x
  def x(i)          : return i.mine
  def setX(i,new)   : i.mine=new
 
@ok
def test1()
  assert yourFirstClass(1).x == 1

def f1(n) :
   if n < 2 : 
     return 1
   else:
     return  f1(n-2) + f1(n-1)

@ok
def test2():
  assert f1(31) == 8222838654177922817725562880000000

def test3(): 
  "simple loop"
  for x in ["m","f","c"]:
    print(x)
    
########

def odd(x)      : return x % 2 == 1
def largeOdd(x) : return odd(x) and x > 10 

def lcomp():
  "example of list comprehension"
  print([x for x in 
           xrange(60,110,3) if largeOdd(x)])

########

@ok 
def bigguns0():
   lst = [8347, 6230, 923834, 1, 404, 993]
   out = [x for x in lst if x > 1000]
   assert out == [6230, 8347, 923834]
   
def bigguns(lst,n):
  "defining inerators"
  lst = sorted(lst)
  for x in lst:
    if x > n:
      yield x

@ok
def biggunsok1():
  "using iterators"
  lst = [8347, 6230, 923834, 1, 404, 993]
  out = []
  for x in bigguns(lst, 1000)
    out += [x]
  assert out == [6230, 8347, 923834]

@ok
def biggunsok2():
  "using iterators"
  lst = [8347, 6230, 923834, 1, 404, 993]
  out = []
  out = [x for x in bigguns(lst, 1000)]
  assert out == [6230, 8347, 923834]

def dict1(d):  print ["c"]

def sorteddict(d):
  "example of walking a dictinary in key sort order"
  for key in sorted(d.keys()):
    yield key, d[key]

@ok 
def sorteddictok():
  d = dict(zip=27615,city='raleigh',state='nc',country='usa')
  assert [key for key,_ in sorteddict(d)] == [
         'city','country','state','zip']]


def myOdds() :
  for x in xrange(60,110,3):
    if odd(x):
      yield(x)

def _iterate():
  "example of defining your own iterator"
  for y in myOdds():
    if y> 90:
      break
    print y

    
root = math.sqrt

x=2


def _x():
  "example of global"
  print x

def fred(y,x=100,
         z=2,pretty = lambda x: int(x)):
  "e.g.1) var scope; 2) code as data"
  print y+z
  print "x",x
  print "pretty",pretty(y+z)
  print root(100)

def _fred(): fred(20)

def _fred1():
  "example of passing code as data"
  fred(22.99,pretty = lambda x: x)

    
def _string1(fruit="banana"):
  index = 0 
  while index < len(fruit): 
    letter = fruit[index] 
    say(letter) 
    index = index + 1 


import string
def _string2():
  "finds 'na' at '2' (i.e. third arg)"
  print string.find("banana", "na")


def _string3():
  "as above, but starts at 3"
  print string.find("banana", "na", 3)


def _string4():
  "fails: specificed range has no 'na'"
  print string.find("banana", "na", 2,3)


def _whites():
  print "[" + string.whitespace+"]"
  for ch in string.whitespace:
    print ord(ch),"["+ch+"]"


def _lowers():
  print string.lowercase


def isLower1(ch="a"):
  print string.find(string.lowercase, ch) != -1


def isLower2(ch="b"):
  print ch in string.lowercase


def isLower3(ch="c",banner="hekko there"):
  print banner,'a' <= ch <= 'z'


def _test1():
  isLower3(banner="work more on python",ch="D")


def _slice():
  a=[1,2,3,4]
  print 0,a[0]
  print 1,a[1:]
  print 2,a[:2]
  print 1,3,a[1:3]
  print -1,a[-1]
    

def _alias():
  a = [1, 2, 3]
  b = a
  a[0]=100
  print a,b
  

def _clones():
  a = [1, 2, 3]
  b = a[:]
  a[0]=100
  print a,b
    
def _dict():
  inventory = {'apples': 430,
               'bananas': 312, 'oranges': 525,
               'pears': 217}
  print "\n:all",inventory
  del inventory['pears']
  print "\n:less",inventory
  print "\n:keys",inventory.keys()
  print "\n:values",inventory.values()
  print "\n:parts",inventory.items()
  print "\n:iterate"
  for key,value in inventory.items():
    print ":key",key,":value",value
    

def _counts():
  seen = {}
  for letter in "Mississippi":
    seen[letter] = seen.get(letter, 0) + 1
    print seen

import copy

class Holds(dict):
  """Dictionary with a default value for unknown keys."""
  def __init__(self, default):
    self.default = default
        
  def __getitem__(self, key):
    if key in self: return self.get(key)
    return self.setdefault(key, copy.deepcopy(self.default))    

def args(*args):
   print args

#@go
def _args() : print args(1,2,3,4,5)

def memo(f):
  memo = {}
  def wrapper(*args):
    if args in memo:
      return memo[args]
    else:
      tmp = f(*args)
      memo[args] = tmp
    return tmp
  return wrapper

@memo
def f2(n) :
    return n if n < 2 else f2(n-2) + f2(n-1)
  

def _f2() : print 320,f2(320)

def _f2slow(): print 320,f1(320)


def _holds1():
  d = Holds(0)
  d['hello'] += 1
  print d

def _holds2():
  d2 = Holds([])
  d2[1].append('hello')
  d2[2].append('world')
  d2[1].append('there')
  print d2


if len(sys.argv)> 1:
  f = sys.argv[1]
  print f
  eval(f + '()')