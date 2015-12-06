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
    def __init__(i,inits, value=same, big=0.025):
        i.big, one, i.values,i.value = big,inits[0],[],value
        example= value(one)
        i.n    = len(example)
        i.lo   = [0 for _ in example]
        i.hi   = [0 for _ in example]
        map(i.update,inits)
        i.east = i.furthest(one)
        i.west = i.furthest(i.east)
        i.c    = i.dist(i.east,i.west)
    def update(i,one):
        i.values += [one]
        for n,(lo,hi,new) in enumerate(zip(i.lo,i.hi,
                                          i.value(one))):
            if new > hi: i.hi[n] = new
            if new < lo: i.lo[n] = new
    def furthest(i,one):
        d, out = 0, one
        for two in i.values:
            tmp = i.dist(one,two)
            if tmp > d:
                d,out = tmp,two
        return out
    def dist(i,xs,ys,d=0):
        for n,(x,y,lo,hi) in enumerate(zip(i.value(xs),
                                           i.value(ys),
                                           i.lo,i.hi)):           
            x  = (x - lo)/(hi - lo + 0.001)
            y  = (y - lo)/(hi - lo + 0.001)
            d += (x - y)**2
        return sqrt(d) / sqrt(i.n)
    def grow(i,east,west):
        print("-",end="")
        b4, i.east, i.west = i.values, east,west
        i.c = i.dist(i.east,i.west)
        i.values[:] = [] 
        map(i.__add__,[i.east,i.west]+b4)
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
            x  = (a**2 + i.c**2 - b**2) / (2*i.c)
            if x > a:
                x = a
            y  = sqrt(a**2 - x**2)
            one.a, one.b, one.x, one.y = a,b,x,y
            one.easterly = a<b
            return x,y
    def half(i,easterly=True):
        return [x for i.values if x.easterly==easterly]
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
                
model=ZDT1()
m=0
seed(12)
decs = lambda x:x.decs
grid=XY([model.one() for _ in range(32)],
        value=decs)
for _ in range(10000):   
    x = model.one()
    y = model.one()
    grid + x
    grid + y
    if model.bdom(x,y): m += 1
print(m,len(grid.values))
print(grid.bounds())
print(grid.east.x,grid.east.y)
print(grid.west.x,grid.west.y)

graph_it(grid.values,model,grid.bounds())
print(len([_ for x in grid.values if x.easterly]))

#for one in grid.values:
 #   print(one.x,one.y)
