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

z=ZDT1()
m=0
for _ in range(1000):
    x = z.one()
    y = z.one()
    if z.bdom(x,y): m += 1
print(m)

#y = z()
#print(z.eval(x))
