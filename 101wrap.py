import datetime

"""

# Example of using Wrapper

## Timing functions

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

## Fibonacci (the Wrong Way)

The following dobly-recursive version blows up after n> 32.

"""
def slowFib(n):
  return 1 if n<2 else slowFib(n-1) + slowFib(n-2)
"""

## Wrapper magic

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

## And does this work?

"""
def demo():
  for n in [10,20,30,32]:
    print "slowFib %s %g secs" % (n, speed(lambda : slowFib(n)))
  print ""
  for n in [10,20,30,32,64,128,256,512]:
    print "fastFib %s %g secs" % (n, speed(lambda : fib(n)))

demo()
"""

## Output

The slow way starts blowing up at 30. Warning. Do not run this for n=33

  > python 101wrap.py
  
  slowFib 10 4.56e-05 secs
  slowFib 20 0.0033521 secs
  slowFib 30 0.516437 secs
  slowFib 32 1.49789 secs
  
The fast way (with memoing) just keeps on trucking.

  fastFib 10 9.3e-06 secs
  fastFib 20 7.4e-06 secs
  fastFib 30 8e-06 secs
  fastFib 32 5.4e-06 secs
  fastFib 64 4.02e-05 secs
  fastFib 128 2.8e-05 secs
  fastFib 256 4.31e-05 secs
  fastFib 512 9.69e-05 secs
  
"""