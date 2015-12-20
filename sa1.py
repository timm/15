from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True
import random,math

r      = random.random
any    = random.choice
within = random.uniform
rseed   = random.seed
sqrt   = math.sqrt
exp    = math.exp

def r3(x)    : return round(x,3)
def r3s(lst) : return map(r3,lst)
def r4(x)    : return round(x,4)
def r4s(lst) : return map(r4,lst)
def r5(x)    : return round(x,5)
def r5s(lst) : return map(r5,lst)

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
        i.evals = 0
    def decide(i,retries=20):
      assert retries>0,'cannot satisfy constraints'
      x      = o(decs=[f() for f in i.decs])
      x.objs = None
      return x if i.ok(x) else i.decide(retries-1) 
    def eval(i,x):
        x.objs = [f(x) for f in i.objs]
        i.evals += 1
        return x
    def one(i):
        return i.eval(i())
    def ok(i,x):
      return True
    def bdom(i,x,y):
        betterOnce = False
        for u,v,meta in zip(x.objs,y.objs,i.objs):
            if meta.better(u,v):
                betterOnce=True
            elif u != v:
                return False
        return betterOnce

class Num:
  def __init__(i,inits=[]):
    i.hi = i.lo = None
    i.mu = i.sd = i.m2 = 0  
    i.n = 0 
    map(i.__add__,inits)
  def __add__(i,x):
    i.n  += 1
    i.lo  = min(z,i.lo)
    i.hi  = max(z,i.hi)
    delta = z - i.mu;
    i.mu += delta/i.n
    i.m2 += delta*(z - i.mu)
    if i.n > 1:
      i.sd = (i.m2/(i.n - 1))**0.5
  def norm(i,z):
    return (z - i.lo) / (i.hi - i.lo + 10e-32)

class Nums:
  def __init__(i,parts):
    i.parts=parts
    i.nums=[Num() for _ in parts]
  def __add__(i,x):
    for x,num in zip(i.parts(x),i.nums):
      num + x
      

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


# meed hi los on decsions and objectives

class Space:
  def __init__(i,one,value=same):
    i.value = value
    i.cache = {}
    lst     = value(one)
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
  def dist1(i,xs,ys,d=0,n=0):
    one = i.value(xs)
    two = i.value(ys)
    for n,(x,y) in enumerate(zip(one,two)):
      x  = i.norm(x,n) 
      y  = i.norm(y,n) 
      d += (x - y)**2
      n += 1
    return sqrt(d) / sqrt(n)
  def norm(i,x,n):
    lo = i.lo[n]
    hi = i.hi[n]
    return (x- lo)/ (hi - lo + 0.0001)
  def furthest(i,one,all):
    d, out = 0, one
    for two in all:
      tmp = i.dist(one,two)
      if tmp > d:
        d,out = tmp,two
    return out

class Log:
  "Holds individuals, knows their geometry."
  def __init__(i,inits, value=same,
               big=0.025,bins=10,space=None):
    i.big, one, i.value,i.values = big,inits[0],value,inits[:]
    i.bins = bins
    i._pos  = {}
    i.space = space or Space(one,value=value)
    i.cells   = [[[] for _ in range(bins)]
                for _ in range(bins)]
    map(i.space.update,inits)
    i.east = i.space.furthest(one,    i.values)
    i.west = i.space.furthest(i.east, i.values)
    i.grow(i.east,i.west)
  def grow(i,east,west):
    print("_",end="")
    b4,i.east, i.west = i.values[:],east,west
    i.c = i.space.dist(i.east,i.west)
    i._pos      = {}
    i.cells     = [[[] for _ in range(i.bins)]
                   for _ in range(i.bins)]
    map(i.__add__,[i.east,i.west]+b4)
  def __add__(i,one):
    a = i.space.dist(i.east,one)
    b = i.space.dist(i.west,one)
    if  a - i.c > i.big:
      i.grow(i.east,one)
      return i + one
    elif b - i.c > i.big:
      i.grow(one,i.west)
      return i + one
    else:
      i.space.update(one)
      x = (a**2 + i.c**2 - b**2) / (2*i.c)
      if x > a:
        x = a
      y = sqrt(a**2 - x**2)
      binx, biny = i.bin(x), i.bin(y)
      i.cells[ binx ][ biny ] += [one]
      i.values += [one]
      i._pos[id(one)] = o(x=x,y=y,binx=binx,
                          biny=biny,a=a,b=b)
      return x,y
  def bin(i,x):
    x = int(x/(i.c/i.bins))
    return min(i.bins - 1, x)
  def pos(i,x) :
    return i._pos[id(x)]
  def clone(i,inits=[]):
    return Log(inits, value=i.value,
                      big=i.big,bins=i.bins, space=i.space)
  def best(i,want,most=0.33,cmp=lt):
    print(i.east is want)
    if east is want:
      return i.clone([x for x in i.values if
                      i.pos(x).a/i.pos(x).b < most])
    else:
      return i.clone([x for x in i.values if
                      i.pos(x).a/i.pos(x).b >  (1 - most)])
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

def mutate(one,log=None,p=0.33, value=same,evaluate=None,ok=None,retries=20):
  tmp= o(decs = [mutate1(old,p,log.space.lo[n],log.space.hi[n])
                   for n,old
                   in enumerate(value(one))])
  if ok:
    assert retries > 0,'too hard to satisfy constraints'
    if not ok(tmp):
      return mutate(one,
                    log=log,p=p, value=value,
                    evaluate=evaluate, ok=ok,
                    retries=retries - 1)
  return evaluate(tmp) if evaluate else tmp

def mutate1(old,p,lo,hi):
  x = (hi - lo)
  y = old if p >= r() else old - x + 2 * x * r()
  return bound(y,lo,hi)

def bound(x, lo, hi):
  return lo + ((x - lo) % (hi - lo))

def decs(x): return x.decs
def objs(x): return x.objs
    
def normmean(log,lst):
  lst = [log.space.norm(x,n) for n,x in enumerate(lst)]
  return sum(lst)/ len(lst)

def saTime(kmax,era,cooling,reports):
  sb = eb = None
  for k in xrange(kmax):
    now = int(k/era)
    if not now in reports:
      if (now - 1) in reports:
        old = reports[now-1]
        sb  = old.sb
        eb  = old.eb
        print("%4d" %k,r4(old.eb)," ",
              o(lt=old.lt,stagger=old.stagger,better=old.better),
              end="")
        print(("  * %f" % eb) if old.better > 0 else "")
      reports[now] = o(lt=0,stagger=0,eb=eb,sb=sb,better=0, e=[])
    t= ((k+1)/kmax)**cooling
    yield t, reports[now]

def optimize(model,how,seed=1,init=10,**d):
  rseed(seed)
  inits   = [model.decide() for one in xrange(init)]
  logDecs = Log(inits,                 value=decs)
  logObjs = Log(map(model.eval,inits), value=objs)
  return how(model,inits,logDecs,logObjs, **d)
  
def sa(model,_,
       logDecs,logObjs,
       era=50,
       kmax=1000, 
       aggr=normmean,
       cooling=2,retries=20,
       p=0.1):
  sb =  s = model.decide()
  eb = e = aggr(logObjs,model.eval(s).objs)
  reports = {}
  for t,report in saTime(kmax,era,cooling,reports):
    sn  = mutate(s,
                 p        = p,
                 ok       = model.ok,
                 log      = logDecs,
                 value    = decs,
                 retries  = 20,
                 evaluate = model.eval)
    logDecs + sn
    logObjs + sn
    en  = aggr(logObjs,sn.objs)
    if en < eb:
      eb = en
      report.better += 1
      report.sb = sn
      report.eb = en
    if en < e:
      s,e = sn,en
      report.lt += 1
    elif exp((e - en)/t) < r():
      s,e = sn,en
      report.stagger += 1
    report.e += [e]
  return report,reports
  
def de(model,frontier,logDecs,logObjs,era=50,repeats=10,cf=0.3,f=0.25):
  for r in xrange(repeats):
    nextgen=[]
    print(r,len(frontier))
    for n,parent in enumerate(frontier):   
      child = smear(frontier,log=logDecs,f=f,cf=cf,evaluate=model.eval)
      logDecs + child
      logObjs + child
      nextgen += [child if model.bdom(child,parent) else parent]
      #elif not model.bdom(parent,child):
       # frontier.append(child)
    frontier = nextgen
  print("\n",model.evals)
  return frontier

def smear(all,log=None,f=0.25,cf=0.5,ok=None,retries=20,evaluate=None):
  aa, bb, cc = any(all), any(all), any(all)
  tmp= o(decs = [smear1(a,b,c,f,cf,log.space.lo[n],log.space.hi[n])
                   for n,(a,b,c)
                   in enumerate(zip(aa.decs,
                                    bb.decs,
                                    cc.decs))])
  if ok:
    print(retries)
    assert retries>0,'too hard to satisfy constraints'
    if not ok(tmp):
      return smear(all,log=log,f=f,cf=cf,ok=ok,
                   retries=retries-1,
                   evaluate=evaluate)
  return evaluate(tmp) if evaluate else tmp

def smear1(a,b,c,f,cf,lo,hi):
  return bound(a + f*(b - c) if r()< cf else a, lo, hi)


rseed(1)
last,all= optimize(ZDT1(),sa,init=100)
print("\n",last.eb,all[0].eb,"\n",all[0].e[0],last.sb.objs)

rseed(1)
optimize(ZDT1(),de,init=10)

exit()

def gale0(model,repeats=100):
  pop  = Log([model() for _ in xrange(repeats)],
                    value=decs)
  for _ in range(10):
    print(smear(pop.values,
                lo = pop.space.lo,
                hi = pop.space.hi,
                value=decs))
  #for i in pop.values:
   # print("z",pop.pos(i).x,
    #      pop.pos(i).y)
  


exit()
  
gale0(ZDT1())

exit()
model=ZDT1()
m=0
seed(12)
decs = lambda x:x.decs
grid=Log([model.one() for _ in range(32)],
        value=decs)
for _ in range(1000):   
    x = model.one()
    y = model.one()
    grid + x
    grid + y
    if model.bdom(x,y): m += 1
want = 0.3
want = 1 - want if model.bdom(grid.west,grid.east) else want

grid1 = grid.half(easterly)

print("")
print(r3s(grid.space.lo))
print(r3s(grid1.space.lo))

print(r3s(grid.space.hi))
print(r3s(grid1.space.hi))

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


