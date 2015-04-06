from __future__ import division,print_function
from lib import *

@setting
def SAMPLE(**d): return o(
    cache = 128
  ).add(**d)

class Cache:
  def __init__(i, init=[], size=None):
    i.max = size or the.SAMPLE.cache
    i.n, i.all, i.ordered = 0, [], False
    map(i.__add__,init)
  def __add__(i,x):
    i.ordered = False
    i.n += 1
    now  = len(i.all)
    if now < i.max:
      i.all += [x]
    elif r() <= now/i.n:
      i.all[ int(r() * now) ]= x
    return i

class SortedCache:
  def __init__(i,init=[],size=None):
    i._cache, i.sorted = Cache(init,size), False
  def __iadd__(i,x):
    i._cache += x
    i.sorted  = False
    return i
  def cached(i):
    if not i.sorted:
      i._cache.all = sorted(i._cache.all)
    i.sorted = False
    return i._cache.all
