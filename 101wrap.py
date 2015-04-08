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

demo()
"""

## Output

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

"""