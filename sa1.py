from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True
import random,math


r    = random.random
any  = random.choice
seed = random.seed
sqrt = math.sqrt

def r3(x)    : return round(x,3)
def r3s(lst) : return map(r3,lst)

class o:
  def __init__(i,**d)    : i.__dict__.update(d)
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __getitem__(i,k)   : return i.__dict__[k]
  def __repr__(i)        : return 'o'+str(i.__dict__)
  def setOnce(i,k,v) :
    if not k in i.__dict__:
      i.__dict__[k] = v

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
        betterOnce = False
        for u,v,meta in zip(x.objs,y.objs,i.objs):
            if meta.better(u,v):
                betterOnce=True
            elif u != v:
                return False
        return betterOnce

class ZDT1(Model):
  n=30
  def about(i):
    def f1(x):
      return x.decs[0]
    def f2(x):
      g = 1 + 9 * sum(x for x in x.decs[1:] )/(ZDT1.n-1)
      return  g * abs(1 - sqrt(x.decs[0]*g))
    def dec(x):
      return An(x,lo=0,hi=1)
    i.decs = [dec(x) for x in range(ZDT1.n)]
    i.objs = [Less("f1",maker=f1),
              Less("f2",maker=f2)]

class Deltas:
  def __init__(i,one,value=same):
    i.value = value
    i.cache = {}
    lst     = value(one)
    i.n     = len(lst)
    i.lo    = [0 for _ in lst]
    i.hi    = [0 for _ in lst]
    i.update(one)
  def update(i,one):
    for n,(lo,hi,new) in enumerate(zip(i.lo, i.hi,
                                       i.value(one))):
      if new > hi: i.hi[n] = new
      if new < lo: i.lo[n] = new
  def dist(i,xs,ys):
    a, b = id(xs), id(ys)
    if a > b:
      return i.dist(ys,xs)
    k = (a,b)
    if k in i.cache:
      return i.cache[k]
    else:
      i.cache[k] = d = i.dist1(xs,ys)
      return d
  def dist1(i,xs,ys,d=0):
    one = i.value(xs)
    two = i.value(ys)
    for n,(x,y,lo,hi) in enumerate(zip(one,two,
                                       i.lo,i.hi)):           
      x  = (x - lo)/(hi - lo + 0.001)
      y  = (y - lo)/(hi - lo + 0.001)
      d += (x - y)**2
    return sqrt(d) / sqrt(i.n)
  def furthest(i,one,all):
    d, out = 0, one
    for two in all:
      tmp = i.dist(one,two)
      if tmp > d:
        d,out = tmp,two
    return out

class XY:
  def __init__(i,inits, value=same, big=0.025,bins=10):
    i.big, one, i.values,i.value = big,inits[0],[],value
    i.bins = bins
    i.deltas = Deltas(one,value=value)
    i.cells   = [[[] for _ in range(bins)]
                for _ in range(bins)]
    map(i.update,inits)
    i.east = i.deltas.furthest(one,    i.values)
    i.west = i.deltas.furthest(i.east, i.values)
    i.c    = i.deltas.dist(i.east,i.west)   
  def update(i,one):
    i.values += [one]
    i.deltas.update(one)
  def grow(i,east,west):
    print("-",end="")
    b4, i.east, i.west = i.values, east,west
    i.c = i.deltas.dist(i.east,i.west)
    i.values[:] = []
    i.cells   = [[[] for _ in range(i.bins)]
                for _ in range(i.bins)]
    map(i.__add__,[i.east,i.west]+b4)
  def __add__(i,one):
    a = i.deltas.dist(i.east,one)
    b = i.deltas.dist(i.west,one)
    if  a - i.c > i.big:
      i.grow(i.east,one)
      return i + one
    elif b - i.c > i.big:
      i.grow(one,i.west)
      return i + one
    else:
      i.update(one)
      x  = (a**2 + i.c**2 - b**2) / (2*i.c)
      if x > a:
        x = a
      y = sqrt(a**2 - x**2)
      one.a, one.b, one.x, one.y = a,b,x,y
      x1,y1= int(x/(i.c/i.bins)), int(y*i.bins)
      x1   = min(i.bins - 1, x1)
      y1   = min(i.bins - 1, y1)
      i.cells[x1][y1] += [one]
      one.easterly = a<b
      return x,y
  def half(i,easterly=True):
    inits = [x for x in i.values
              if x.easterly==easterly]
    return XY(inits,
              value=i.value,big=i.big,bins=i.bins)
  def bounds(i):
    xs= sorted([one.x for one in i.values])
    ys= sorted([one.y for one in i.values])
    return (xs[0]*0.95,xs[-1]*1.05),(ys[0]*0.95,ys[-1]*1.05)
    
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def graph_it(population, model, scale):
    directory = 'models/'
    file_name = directory + model.__class__.__name__
    f1 = np.array([one.x for one in population])
    f2 = np.array([one.y for one in population])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(f1, f2, s = 40, color = '#000080', alpha=0.80)
    ax.set_xlim(scale[0])
    ax.set_ylim(scale[1])
    ax.set_xlabel('f1')
    ax.set_ylabel('f2')
    fig.savefig(file_name)

def gale0(model,repeats=256):
  decs = lambda x:x.decs
  grid = XY([model() for _ in xrange(repeats)],
            value=decs)
  for _ in range(10):
    grid= grid.half(
            model.bdom(grid.east,grid.west))


  def smear(all,lo,hi,f=0.25,cf=0.5,value=same):
  as,bs,cs = any(all), any(all), any(all)
  tmp =[smear1(a,b,c,n)
        for n,(a,b,c)
        in  enumerate(zip(as.decs,
                          bs.decs,
                          cs.decs))]
  return o(decs=tmp)
  
def smear1(a,b,c,n):
  return bound(a + f*(b - c) if r()< cf else a,
               lo[n], hi[n])

def bound(x, lo, hi):
  return (((x - lo) % (hi - lo)) + lo)

gale0(ZDT1())

exit()
model=ZDT1()
m=0
seed(12)
decs = lambda x:x.decs
grid=XY([model.one() for _ in range(32)],
        value=decs)
for _ in range(1000):   
    x = model.one()
    y = model.one()
    grid + x
    grid + y
    if model.bdom(x,y): m += 1
easterly = model.bdom(grid.east,grid.west)

grid1 = grid.half(easterly)

print("")
print(r3s(grid.deltas.lo))
print(r3s(grid1.deltas.lo))

print(r3s(grid.deltas.hi))
print(r3s(grid1.deltas.hi))

print("grdi1",m,len(grid.values))
print(grid.bounds())
print(grid.east.x,grid.east.y)
print(grid.west.x,grid.west.y)

graph_it(grid.values,model,grid.bounds())
print(len([_ for x in grid.values if x.easterly]))

#for one in grid.values:
 #   print(one.x,one.y)

for n1,x in enumerate(grid.cells):
  for n2,y in enumerate(x):
    if y:
      print(n1,n2,len(y))


a=o(b=1,c=2)

a.setOnce('b',10)
a.setOnce('d',10)
a.setOnce('d',11)
print(a)


