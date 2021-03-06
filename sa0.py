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
    def __init__(i,east,west,big=0.025,values=[],value=same):        
        i.values, i.value, i.big = values, value, big
        example    = value(east)
        i.w        = len(example)
        i.lo,i.hi  = [0 for _ in example], [0 for _ in example]
        i.one,i.east, i.west = east,east,west     
        i.update(east)
        i.update(west)
        i.c = i.dist(i.east,i.west)
    def update(i,one):
        i.values += [one]
        for n,(lo,hi,new) in enumerate(zip(i.lo,i.hi,
                                          i.value(one))):
            if new > hi: i.hi[n] = new
            if new < lo: i.lo[n] = new
    def dist(i,xs,ys,d=0):
        for n,(x,y,lo,hi) in enumerate(zip(i.value(xs),
                                           i.value(ys),
                                           i.lo,i.hi)):           
            x  = (x - lo)/(hi - lo + 0.001)
            y  = (y - lo)/(hi - lo + 0.001)
            d += (x - y)**2
        return sqrt(d) / sqrt(i.w)
    def grow(i,east,west):
        print("-",end="")
        b4, i.east, i.west = i.values, east,west
        i.c = i.dist(i.east,i.west)
        print("!",end="")
        if i.c > 1:
            print(i.c,i.value(i.east),i.value(i.west))
        i.values[:] = [] 
        map(i.__add__,b4)
    def __add__(i,one):
        a = i.dist(i.east,one)
        b = i.dist(i.west,one)
        if  a - i.c > i.big:
            i.grow(i.east,one)
            return i + one
        elif b - i.c > i.big:
            i.grow(one,i.west)
            return i + one
        else:
            i.update(one)
            c  = i.c
            i.c = min(i.c,1)
            x  = (a**2 + c**2 - b**2) / (2*c)
            x  = min(x,a)
            
            if x>a:
                print(a,b,c,x)
            y  = sqrt(a**2 - x**2)
            one.x, one.y = x,y
            return x,y

z=ZDT1()
m=0
f = lambda x:x.decs
grid=XY(z.one(),z.one(),value=f)
for _ in range(100):   
    x = z.one()
    y = z.one()
    grid + x
    grid + y
    if z.bdom(x,y): m += 1
print(m,len(grid.values))
for one in grid.values:
    print(one.x,one.y)
