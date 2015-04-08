import datetime

"""

# Markdown

asdas
asdas

## asdas

asa

"""

def speed(f,n=10):
  start = datetime.datetime.now()
  for _ in xrange(n):
    last = f()
  stop = datetime.datetime.now()
  delta = (stop - start).total_seconds()
  return delta/(n*1.0)

def slowFib(n):
  return 1 if n<2 else slowFib(n-1) + slowFib(n-2)


def memo(func):
  cache = {} # build at load time
  def memoedFunc(*args): # called at load time
    if args not in cache:
      cache[args] = func(*args)
    return cache[args]
  return memoedFunc

@memo
def fib(n):
  return 1 if  n<2 else fib(n-1) + fib(n-2)

def demo():
  for n in [10,20,30,32]:
    print "slowFib %s %g secs" % (n, speed(lambda : slowFib(n)))
  print ""
  for n in [10,20,30,32,64,128,256,512]:
    print "fastFib %s %g secs" % (n, speed(lambda : fib(n)))

demo()
