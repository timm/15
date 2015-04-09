from __future__ import print_function,division
from unittest import *
import math

class yourFirstClass:
  "init is called when created"
  def __init__(i,x) : i.mine = x
  def x(i)          : return i.mine
  def setX(i,new)   : i.mine=new
 
@ok
def go1():
  assert yourFirstClass(1).x == 1 

class Holds(dict):
  "Dictionary with a default value for unknown keys."
  def __init__(i, default):
    if not  callable(default):
      default = lambda : default
    i.default = default
  def __getitem__(i, key):
    if key in i: return i.get(key)
    return i.setdefault(key,  i.default())    

@ok
def go0():
  h = Holds(0)
  assert 1 == 1 + h["a"]
  assert h["a"] == 1

print(h['a'] + 1)

#################
# your first function

def f1(n) :
   if n < 2 : 
     return 1
   else:
     return  f1(n-2) + f1(n-1)

@ok
def go2():
  assert f1(31) == 8222838654177922817725562880000000 

def test3(): 
  "simple loop"
  out = ""
  for x in ['m','f','c']:
    out += x
  assert out == 'mfc'
    
########
def funWithDefaults(n,name='tim', age=54,showsize=12):
    return (n,name,age,shoesize)
    
@ok 
def go3():
  assert (10,'tom',20,12) == funWithDefaults(
                           10,age=20,name='tom') 
                           
def callingVars(*lst,**dic):
  return (lst,dic)
  
@ok 
def go4(): 
  assert callingVars(
          1,2,3,name='tim',age=54,shoesize=12) == (
          [1,2,3], 
          {'name':'tim','age':54,'shoesize':12}
          )
    
########

def odd(x)      : return x % 2 == 1
def largeOdd(x) : return odd(x) and x > 10 

@ok
def go5():
  "example of list comprehension"
  assert [63, 69, 75, 81, 87, 93, 99, 105] == [
          x for x in xrange(60,110,3) if largeOdd(x)]

########

@ok 
def go6():
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
def go7():
  "using iterators"
  lst = [8347, 6230, 923834, 1, 404, 993]
  out = []
  for x in bigguns(lst, 1000):
    out += [x]
  assert out == [6230, 8347, 923834]

@ok
def go8():
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
def go9():
  d = dict(zip=27615,city='raleigh',state='nc',country='usa')
  assert [key for key,_ in sorteddict(d)] == [
         'city','country','state','zip']

 
import string
  
def _string2():
  "finds 'na' at '2' (i.e. third arg)"
  print(string.find("banana", "na"))


def _string3():
  "as above, but starts at 3"
  print(string.find("banana", "na", 3))


def _string4():
  "fails: specificed range has no 'na'"
  print(string.find("banana", "na", 2,3))


def _whites():
  print("[" + string.whitespace+"]")
  for ch in string.whitespace:
    print(ord(ch),"["+ch+"]")


def _lowers():
  print(string.lowercase)


def isLower1(ch="a"):
  print(string.find(string.lowercase, ch) != -1)


def isLower2(ch="b"):
  print(ch in string.lowercase)


def isLower3(ch="c",banner="hekko there"):
  print(banner,'a' <= ch <= 'z')


def _test1():
  isLower3(banner="work more on python",ch="D")


def _slice():
  a=[1,2,3,4]
  print(0,a[0])
  print(1,a[1:])
  print(2,a[:2])
  print(1,3,a[1:3])
  print(-1,a[-1])
    

def _alias():
  a = [1, 2, 3]
  b = a
  a[0]=100
  print(a,b)
  

def _clones():
  a = [1, 2, 3]
  b = a[:]
  a[0]=100
  print(a,b)
    
def _dict():
  inventory = {'apples': 430,
               'bananas': 312, 'oranges': 525,
               'pears': 217}
  print("\n:all",inventory)
  del inventory['pears']
  print("\n:less",inventory)
  print("\n:keys",inventory.keys())
  print("\n:values",inventory.values())
  print("\n:parts",inventory.items())
  print("\n:iterate")
  for key,value in inventory.items():
    print(":key",key,":value",value)
    

def _counts():
  seen = {}
  for letter in "Mississippi":
    seen[letter] = seen.get(letter, 0) + 1
    print(seen)


