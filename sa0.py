from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True
import random,math


r = random.random
seed = random.seed
sqrt = math.sqrt

class o:
  def __init__(i,**d)    : i.__dict__.update(d)
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __getitem__(i,k)   : return i.__dict__[k]
  def __repr__(i)        : return 'o'+str(i.__dict__)

def same(x): return x
def lt(x,y): return x < y
def gt(x,y): return x > y

class Objective:
  def __init__(i,txt,maker=None,better=lt):
      i.better = better
      i.txt,i.maker = txt,maker
  def __call__(i,x):
      return i.maker(x)

def More(*l,**d): return Objective(*l,better=gt,**d)
def Less(*l,**d): return Objective(*l,better=lt,**d)
    
class Decision:
    def __init__(i,str,lo=None,hi=None):
        i.str,i.lo,i.hi = str,lo,hi
    def __call__(i):
        return i.lo + r()*(i.hi - i.lo)

An = A = Decision

class Model:
    def __init__(i):
        i.about()
    def __call__(i):
        x      = o(decs=[f() for f in i.decs])
        x.objs = None
        return x
    def eval(i,x):
        x.objs = [f(x) for f in i.objs]
        return x
    def one(i):
        return i.eval(i())
    def bdom(i,x,y):
        better1 = False
        for u,v,meta in zip(x.objs,y.objs,i.objs):
            if meta.better(u,v):
                better1=True
            elif u != v:
                return False
        return better1

class ZDT1(Model):
  n=30
  def about(i):
    def f1(x):
      return x.decs[0]
    def f2(x):
      g = 1 + 9*sum(x for x in x.decs[1:] )/(ZDT1.n-1)
      return g*abs(1 - sqrt(x.decs[0]*g))
    def dec(x):
      return An(x,lo=0,hi=1)
    i.decs = [dec(x) for x in range(ZDT1.n)]
    i.objs = [Less("f1",maker=f1),
              Less("f2",maker=f2)]

class XY:
    def __init__(i,east,west,big=0.025):
        i.w   = len(east)
        i.lo  = [0] * i.w
        i.hi  = [0] * i.w
        i.big = big
        i.all = []
        i.east, i.west = east,west     
        i.updateRanges(east)
        i.updateRanges(west)
        i.c = i.dist(i.east,i.west)
    def updateRanges(i,lst):
       for n,(lo,hi,new) in enumerate(zip(i.lo,i.hi,lst)):
            if new > hi: i.hi[n] = new
            if new < lo: i.lo[n] = new
    def dist(i,xs,ys,d=0):
        for n,(x,y,lo,hi) in enumerate(zip(xs,ys,i.lo,i.hi)):           
            x  = (x - lo)/(hi - lo + 0.00001)
            y  = (y - lo)/(hi - lo + 0.00001)
            d += (x - y)**2
        return sqrt(d) / sqrt(i.w)
    def grow(i,east,west,b4):
        i.east, i.west = east,west
        i.c = i.dist(i.east,i.west)
        i.all = []
        map(i.__add__,b4)
    def __add__(i,lst):
        a = i.dist(i.east,lst)
        b = i.dist(i.west,lst)
        if  a - i.c > i.big:
            i.grow(i.east,lst,i.all)
            return i + lst
        elif b - i.c > i.big:
            i.grow(lst,i.west,i.all)
            return i + lst
        else:
            i.all += [lst]
            c  = i.c
            x  = (a**2 + c**2 - b**2) / (2*c)
            x1 = min(max(x,1),0)
            y  = sqrt(a**2 - x1**2)
            return x,y

z=ZDT1()
m=0
f = lambda x:x.decs
grid=XY(f(z.one()),f(z.one()))
for _ in range(100000):   
    x = z.one()
    y = z.one()
    grid + f(x)
    grid + f(y)
    if z.bdom(x,y): m += 1
print(m)
