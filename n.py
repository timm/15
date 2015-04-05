from __future__ import division,print_function
from lib import *

class N(): 
  def __init__(i, inits=[], name=None,
               lo=None, hi=None):
    i.n = i.mu = i.m2 = 0; 
    i.w, i.name = 1, (name or 'N')
    i.lo =  10**32 if lo is None else lo
    i.hi = -10**32 if hi is None else hi
    map(i.__iadd__,inits)
  def norm(i,x):
    return (x - i.lo()) / (i.hi() - i.lo() +0.0001)
  def sd(i):
    return 0 if i.n < 2 else (i.m2/(i.n - 1))**0.5
  def pdf(i,z):
    return normpdf(i.mu,i.sd(),z) if i.sd() else 1
  def __iadd__(i,x):
    i.n   += 1
    i.lo   = min(i.lo, x)
    i.hi   = max(i.hi, x)
    delta  = x - i.mu
    i.mu  += delta/i.n
    i.m2  += delta*(x - i.mu)
    return i
  def __isub__(i,x):
    i.lo, i.hi = 10**32, -10**32
    i.n   -= 1
    delta  = x - i.mu
    i.mu  -= delta/i.n
    i.m2  -= delta*(x - i.mu)
    return i
  def __repr__(i): return string(i.__dict__)
