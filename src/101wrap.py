import datetime

"""

## Example of using Function Decorators

_PREFIX/aaa _PREFIX/bb

### Timing functions

How long does it take to run?

"""
def speed(f,repeats=10):
  start = datetime.datetime.now()
  for _ in xrange(repeats): 
    f()
  stop = datetime.datetime.now()
  delta = (stop - start).total_seconds()
  return delta/(repeats*1.0)
"""

### Fibonacci (the Wrong Way)

The following doubly -recursive version blows up after n> 32.

"""
def slowFib(n):
  return 1 if n<2 else slowFib(n-1) + slowFib(n-2)
"""

Of course, we could be clever and carry round the n-1)
result to use with the nth result:

"""
def fasterFib(n):
    a, b = 0, 1
    for i in xrange(n):
        a, b = b, a + b
    return a
"""

But wouldn't it be great if we didn't have to be clever?

### Wrapper magic

Rewrite the function such that old results get cached and,
perhaps, reused.

"""
def memo(func):
  cache = {} # initialized at load time
  def memoedFunc(*args): # called at load time
    if args not in cache:
      cache[args] = func(*args)
    return cache[args]
  return memoedFunc

@memo
def fib(n):
  return 1 if  n<2 else fib(n-1) + fib(n-2)
"""

### And does this work?

"""
def demo():
  for n in [10,20,30,32]:
    print "slowFib %s %g secs" % (
      n, speed(lambda : slowFib(n)))
  print ""
  for n in [10,20,30,32,64,128,256,512]:
    print "fasterFib %s %g secs" % (
      n, speed(lambda : fasterFib(n)))
  print ""
  for n in [10,20,30,32,64,128,256,512]:
    print "fastFib %s %g secs" % (
      n, speed(lambda : fib(n)))

#demo()
"""

### Output

The slow way starts blowing up at 30. Warning. Do not run this for n=33

    > python 101wrap.py
  
    slowFib 10 2.28e-05 secs
    slowFib 20 0.002417 secs
    slowFib 30 0.48794 secs
    slowFib 32 1.31186 secs
    
The faster way (using clever programming) scales better.

    fasterFib 10 6.3e-06 secs
    fasterFib 20 6.8e-06 secs
    fasterFib 30 7.7e-06 secs
    fasterFib 32 7.4e-06 secs
    fasterFib 64 8.9e-06 secs
    fasterFib 128 1.65e-05 secs
    fasterFib 256 2.53e-05 secs
    fasterFib 512 4.63e-05 secs
  
And the simpler way (with memoing) also works fine.
    
    fastFib 10 7.3e-06 secs
    fastFib 20 5.4e-06 secs
    fastFib 30 5.2e-06 secs
    fastFib 32 2.4e-06 secs
    fastFib 64 2.45e-05 secs
    fastFib 128 1.39e-05 secs
    fastFib 256 2.17e-05 secs
    fastFib 512 8.18e-05 secs

## A More Advanced Example

In any clustering system, the thing that
takes the most time is working on the
distance between rows in tables of
data. 

"""
def closest(row, rows):
  "What row is closest within rows?" 
  d, best = 10**32, None
  for x in rows:
    if x != row:
      tmp = row - x # note: distance is "-"
      if tmp < best:
        d, best = tmp, x
  return best
"""

In the above,  we define "i - x" to be
the distance between two items.

One trick for reducing this time is 
to cache distance calcuations such that 
if ever we calcuate i.dist(j) then 
i AND j  remember that dist for 
future reference. We'll call that
"mirroring".

Note that the following code cache's
things in an entry marked with the name
of the calling function. So this cache
can cache things from many different functions.

First, we will do a  basic cache, 
which will serve to illustrate some
of the basic techniques.

"""
def cache(f):
  "Caching, simple case, no mirroring."
  name = f.__name__  
  def wrapper(i):
    if hasnot(i,"_cache"): i._cache = {}  
    key = (name, i.id)
    if key in i._cache:
      x = i._cache[key]
    else:
      x = f(i) # sigh, gonna have to call it
    i._cache[key] =  x # ensure ache holds 'c'
    return x
  return wrapper
"""

Now we repeat the above, modified for the
mirrored cache case.

"""
def cache2(f):
  "Cache mirrored properties."
  name = f.__name__
  def wrapper(i,j):
    if hasnot(i,"_cache"): i._cache = {}  
    if hasnot(j,"_cache"): j._cache = {}
    if i.id > j.id: 
      i,j = j,i # ids now sorted Vv
    key = (name, i.id, j.id) 
    if key in i._cache:
      x = i._cache[key]
    elif key in j._cache:
      x = j._cache[key]
    else:
      x = f(i,j) # sigh, gonna have to call it
    i._cache[key] = j._cache[key] = x
    return x
  return wrapper
"""

One design decision here that is kinda fun
is "where do we put the cache?":

+ In the above `memo` function, we built
  one cache per function, with no way to forget
  outdated information.
+ In the following, we create a Row object 
  and keep the cache in the row. Then, if the 
  row is ever garbage collected then "Zap!",
  its cache goes as well. Neat!

First, here's a little Python magic,
to check if a variable has a certain named
variable.
"""
def hasnot(inst,name):
  "True if instance lacks variable."
  return not name in inst.__dict__
"""

Back to our example of using `cache`
and `cache2`. For that design decision to 
work, we'll have to refer to Rows by some
unique numeric id (and not a pointer... why?)
that is different for each row.

"""
class Row:
  id=0
  def __init__(i, cells):
    assert cells, "needs some cells"
    Row.id = i.id = Row.id + 1 #get a  unique id
    i.cells = cells 
  def __eq__(i,j): return i.id == j.id "i == j"
  def __ne__(i,j): return i.id != j.id "i != j"
  def value(i):
    """Some slow domain specific value function 
    which we'll sub-class for other row types."""
    return slowFib(round((i[0] + i[-1]) / 2.0))
  def __getitem__(i,key): 
    "Implements row[i] (easy access to cells)."
    return i.cells[key]
  def __sub__(i,j):
    "Implements i - j (the distance calc)."
    return i.dist(j)
  def __lt__(i,j):
    "Implements i < j (used in sorting)."
    return i.score() < j.score()
  @cache # single argument cache
  def score(i): 
    return i.value()
  @cache2 # doube argument symmetric caching
  def dist(i,j): 
    "Returns a number 0..1"
    tmp = [(x -y)**2  for x,y in zip(i,j)]
    return sum(tmp)**0.5/ len(tmp)**0.5
"""

### RowDemo

"""
def rowDemo():
  import random
  random.seed(1) 
  cellsPerRow    = 10 # cells perRow
  maxRangeOfCell = 29
  nRows          = 100
  repeats        = 100
  def row1():
    "Make one row"
    return Row([random.random()*maxRangeOfCell 
                for _ in range(cellsPerRow)])
  # make many rows
  some = [row1() for _ in range(nRows)]
  # tests the sorting code
  sorted(some)  
  # test the distance code
  for _ in xrange(repeats):
    for one in some:
      one.nearest = closest(one, some)
      
rowDemo()
