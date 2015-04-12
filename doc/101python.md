[<img width=900 src="https://raw.githubusercontent.com/timm/15/master/src/img/banner.jpg">](https://github.com/timm/15/blob/master/README.md)

_Go to: [Home](https://github.com/timm/15/blob/master/README.md) | [Sitemap](https://github.com/timm/15/blob/master/TOC.md)_


# 101python.py


# 101python.py: some basic Python examples

How to learn Python:

1. read Python code
2. run Python code
3. read Stackoverflow.com, a lot. e.g
   Want to know how to check if a file
   exits? Then Google "stackoverflow python 
   how to check if a file exists".

Anyway, on with this file's code....
_________________________________________________

## Standard start up stuff

This Python 2 code. Which is fine for most
things but the Pyton 3 division and print
stuff is better.

````python
from __future__ import print_function,division
````

Grab some standard utils

````python
import math,string
````

BEFORE reading this code, go away and
read up on the ok.py test engine

````python
from ok import *
````

The rest of this code contains functions
that are called at load time (these are
decorated with "@ok"). Every "assert"
statements checks that the expected
thing is happenning.

_________________________________________________

##  Some String Manipulation

````python
@ok 
def _string2():
  assert 2 == string.find("banana", "na")

@ok 
def _string3():
  "As above, but starts at 3"
  assert 4 == string.find("banana", "na", 3)

@ok 
def _string4():
  "Fails: specificed range has no 'na'" 
  assert -1  == string.find("banana", "na", 2,3)

@ok 
def _lowers():
  "Shows a useful property of 'string'"
  assert string.lowercase == 'abcdefghijklmnopqrstuvwxyz'  

@ok 
def isLower1(ch="a"):
  "A simple test."
  assert string.find(string.lowercase, ch) != -1

@ok 
def isLower2(ch="b"):
  "We lower case?"
  assert ch in string.lowercase

````
_________________________________________________

## Fun with Functions

````python
def f1(n) :
  "Fibanacci. Slow. Want faster? See 101wrap.py."
  if n < 2 : 
    return 1
  else:
    return  f1(n-2) + f1(n-1)

@ok
def f1ok(): 
  assert f1(31) == 2178309 

@ok
def test3(): 
  "simple loop"
  out = ""
  for x in ['m','f','c']:
    out += x
  assert out == 'mfc'

# Functions can have named arguments, with defaults.

def funWithDefaults(n,name='tim', age=54,shoesize=12):
    return (n,name,age,shoesize)
    
@ok 
def go3():
  assert (10,'tom',20,12) == funWithDefaults(
                           10,age=20,name='tom') 
                           
# Internally, those args are dictionaries.
def callingVars(*lst,**dic):
  return (lst,dic)
  
@ok 
def go4(): 
  assert callingVars(
          1,2,3,name='tim',age=54,shoesize=12) == (
          (1,2,3), 
          {'age':54,'name':'tim','shoesize':12})
          
````
_________________________________________________

## Lists, coping, slices

````python
@ok
def _slice():
  "Accessing"
  a = ['a','b','c','d']
  assert 'a'           == a[0]
  assert ['b','c','d'] == a[1:]
  assert ['a','b'] == a[:2]
  assert 'd'           == a[-1]

@ok     
def _alias():
  "Side-effect on updates."
  a    = [1, 2, 3]
  b    = a
  a[0] = 100
  assert b[0] == 100

@ok 
def _clones():
  "Deep copy."
  a = [1, 2, 3]
  b = a[:]
  a[0]=100
  assert b == [1,2,3] 

````
_________________________________________________

## Dictionaries

````python
@ok 
def _dict():
  "Adding, deleting stuff."
  inventory1 = {'apples' : 430,
                'bananas': 312, 
                'oranges': 525,
                'pears'  : 217}
  inventory2 = dict(apples  = 430,
                    bananas = 312, 
                    oranges = 525,
                    pears   = 217)
  assert inventory1 == inventory2 
  del inventory1['pears']
  assert inventory1 == {'apples' : 430,
                        'bananas': 312, 
                        'oranges': 525 }
  assert inventory1.keys() == [
            'apples', 'oranges','bananas']
  assert inventory1.values() == [430, 525, 312]
  assert  [('apples' , 430),
           ('oranges', 525),
           ('bananas', 312)] == inventory1.items()
  assert inventory1 == {key:value for key,value 
                        in inventory1.items()}
    
@ok
def _counts():
  "Using a dict to count character frequencies
  seen = {}
  for x in "Mississippi":
    seen[x] = seen.get(x, 0) + 1
  assert seen == {'i': 4, 'p': 2, 's': 4, 'M': 1}

````
_________________________________________________

## Classes and sub-classes

````python
class yourFirstClass:
  "init is called when created"
  def __init__(i,x) : i.mine = x
  def x(i)          : return i.mine
  def setX(i,new)   : i.mine=new
 
@ok
def go1():
  assert yourFirstClass(1).x() == 1 

# Subclassing

class Holds(dict):
  "Dictionary with a default value for unknown keys."
  def __init__(i, default):
    i.default = default
  def __getitem__(i, key):
    if key in i: 
      return i.get(key)
    else: 
      return i.setdefault(key, i.default)  

@ok
def go0():
  h = Holds(0)
  for x in "Mississippi":
    h[x] += 1
  assert h == {'i': 4, 'p': 2, 's': 4, 'M': 1}

````
_________________________________________________

## Declaractive programming in Python

Build up the processing by writing little primitives
that get combined by other functions.

````python
def odd(x)      : return x % 2 == 1
def largeOdd(x) : return odd(x) and x > 10 

@ok
def go5():
  "example of list comprehension"
  assert [63, 69, 75, 81, 87, 93, 99, 105] == [
          x for x in xrange(60,110,3) if largeOdd(x)]


## "Iterators" let you seperate data filtering from
## data usage. Iterator functions use "yield" and not
## "return"

@ok 
def go6():
  "Without iterators."
   lst = [8347, 6230, 923834, 1, 404, 993]
   out = [x for x in lst if x > 1000]
   assert out == [8347, 6230, 923834]
   
def bigguns(lst,n):
  "Defining iterator"
  lst = sorted(lst)
  for x in lst:
    if x > n:
      yield x

@ok
def go7():
  "Using iterators"
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

def sorteddict(d):
  "example of walking a dictinary in key sort order"
  for key in sorted(d.keys()):
    yield key, d[key]

@ok 
def go9():
  d = dict(zip=27615,city='raleigh',state='nc',country='usa')
  assert [key for key,_ in sorteddict(d)] == [
         'city','country','state','zip']


````

__________

<img width=200 align=right src="https://github.com/timm/15/blob/master/src/img/wtfpl.svg">
Copyright © 2015 Your Name <tim.menzies@gmail.com>

This work is free. You can redistribute it and/or modify it under the
terms of the Do What The F*ck You Want To Public License, Version 2,
as published by Sam Hocevar. See [here](http://www.wtfpl.net/faq/) for more details.
