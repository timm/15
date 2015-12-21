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
      x      = o(objs=None,decs=[f() for f in i.decs])
      x.objs = None
      return x if i.ok(x) else i.decide(retries-1) 
    def eval(i,x):
      if not x.objs:
        x.objs = [f(x) for f in i.objs]
        i.evals += 1
      return x
    def one(i):
        return i.eval(i())
    def ok(i,x):
      return True
    def bdom(i,x,y):
        betters = 0
        for u,v,meta in zip(x.objs,y.objs,i.objs):
            if meta.better(u,v):
                betters += 1
            elif u != v:
                return False,0
        return betters > 0, betters

class Some:
  def __init__(i, init=[], max=256):
    i.n, i.all, i.max = 0,[],max
    map(i.__add__,init)
  def __add__(i,x):
    i.n += 1
    now = len(i.all)
    if now < i.max:
      i.all += [x]
    elif r() <= now/i.n:
      i.all[ int(r() * now) ]= x

class Num:
  def __init__(i,inits=[]):
    i.hi = i.lo = None
    i.mu = i.sd = i.m2 = 0  
    i.n = 0
    i.some = Some()
    i._also= None
    map(i.__add__,inits)
  def __add__(i,z):
    i._also = None
    i.n  += 1
    i.some + z
    i.lo  = min(z,i.lo)
    i.hi  = max(z,i.hi)
    delta = z - i.mu;
    i.mu += delta/i.n
    i.m2 += delta*(z - i.mu)
    if i.n > 1:
      i.sd = (i.m2/(i.n - 1))**0.5
  def norm(i,z):
    return (z - i.lo) / (i.hi - i.lo + 10e-32)
  def also(i):
    if not i._also:
      lst = sorted(i.some.all)
      q   = int(len(lst)/4)
      i._also = o(some=lst,
                  median=lst[2*q],
                  q1 = lst[q],
                  q3 = lst[3*q],
                  range=r3s([lst[0],lst[q],lst[2*q],lst[3*q],lst[-1]]))
    return i._also
  
class Nums:
  def __init__(i,n,parts,inits=[]):
    i.parts=parts
    i.nums=[Num() for _ in xrange(n)]
    map(i.__add__,inits)
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
    if x > i.hi[n]: i.hi[n] = x
    if x < i.lo[n]: i.lo[n] = x
    lo = i.lo[n]
    hi = i.hi[n]
    return (x- lo)/ (hi - lo + 0.0001)
  def furthest(i,one,all,better=gt,most=0):
    d, out = most, one
    for two in all:
      if id(two) != id(one):
        tmp = i.dist(one,two)
        if better(tmp,d):
          d,out = tmp,two
    return out,d
  def closest(i,one,all):
    return i.furthest(one,all,better=lt,most=10**32)

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
    i.east,_ = i.space.furthest(one,    i.values)
    i.west,_ = i.space.furthest(i.east, i.values)
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
  tmp= o(objs=None,
         decs = [mutate1(old,p,log.space.lo[n],log.space.hi[n])
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

def saControl(kmax,era,cooling):
  def newEra():
    return not now in reports
  def startNewEra(sb,eb):
    reports[now] = o(lt=0,stagger=0,eb=eb,sb=sb,better=0, e=[])
  def oldEra():
    return (now - 1) in reports
  def finishOldEra():
    old = reports[now-1]
    sb  = old.sb
    eb  = old.eb
    #print("%4d" %k,r4(old.eb)," ",
     #     o(lt=old.lt,stagger=old.stagger,better=old.better),
      #    end="")
    #print(("  * %s" % sb.objs) if old.better > 0 else "")
    return sb,eb
  #--------------------------------
  sb, eb, reports = None, None, {}
  for k in xrange(kmax):
    now = int(k/era)
    if newEra():
      if oldEra():
        sb,eb = finishOldEra()
      startNewEra(sb,eb)
    t = ((k+1)/kmax)**cooling
    yield t, reports[now],reports

def optimize(model,how,seed=1,init=10,**d):
  rseed(seed)
  print("\n---|",how.__name__,"|-------------------------")
  pop0   = [model.eval(model.decide())
             for one in xrange(init)]
  logDecs = Log(pop0, value=decs)
  logObjs = Log(pop0, value=objs)
  someNums(pop0,logObjs,model)
  pop = how(model,pop0,logDecs,logObjs, **d)
  someNums(pop,logObjs,model)
  return pop0,pop
  
def sa(model,_,
       logDecs,logObjs,
       era=50,
       kmax=1000, 
       aggr=normmean,
       cooling=2,retries=20,
       p=0.1):
  sb = s = model.decide()
  eb = e = aggr(logObjs,model.eval(s).objs)
  for t,now,history in saControl(kmax,era,cooling):
    sn  = mutate(s, p        = p,
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
      now.better += 1
      now.sb, now.eb = sn,en
    if en < e:
      s,e = sn,en
      now.lt += 1
    elif exp((e - en)/t) < r():
      s,e = sn,en
      now.stagger += 1
    now.e += [e]
  return [sb]


def someNums(inits,logObjs,model):
  nums= Nums(len(model.objs)+1,
              lambda x: x.objs+[normmean(logObjs,x.objs)],
              inits)
  print(model.__class__.__name__,
        map(lambda x:x.also().range, nums.nums))
  
def de(model,frontier,logDecs,logObjs,era=50,repeats=10,cr=0.3,f=0.75):
  for r in xrange(repeats):
    for n in xrange(len(frontier)):
      parent = frontier[n]
      child = smear(frontier,log=logDecs,f=f,
                    cr=cr,evaluate=model.eval)
      logDecs + child
      logObjs + child
      if model.bdom(child,parent)[0]:
        frontier[n] = child
      #elif not betters2:
       # frontier.append(child)
  return frontier


def bdoms(model,frontier,*_):
  for x in frontier:
    x.alive = True
  for x in frontier:
    for y in frontier:
      if model.bdom(x,y)[0]:
        y.alive = False
  return [f for f in frontier if f.alive]

def smear(all,log=None,f=0.25,cr=0.5,ok=None,retries=20,evaluate=None):
  aa, bb, cc = any(all), any(all), any(all)
  tmp= o(objs=None,
         decs = [smear1(a,b,c,f,cr,log.space.lo[n],log.space.hi[n])
                   for n,(a,b,c)
                   in enumerate(zip(aa.decs,
                                    bb.decs,
                                    cc.decs))])
  if ok:
    assert retries>0,'too hard to satisfy constraints'
    if not ok(tmp):
      return smear(all,log=log,f=f,cf=cf,ok=ok,
                   retries=retries-1,
                   evaluate=evaluate)
  return evaluate(tmp) if evaluate else tmp

def smear1(a,b,c,f,cr,lo,hi):
  return bound(a + f*(b - c) if r()< cr else a, lo, hi)


def igd(models=[ZDT1],hows=[sa,de,bdoms], repeats=20, seed0=1,init=300):
  for model in models:
    rseed(seed0)
    for how in hows:
      name = how.__name__
      for seed1 in [r() for _ in xrange(repeats)]:
        every    = []
        lasts    = {how.__name__:[] for how in hows}
        rseed(seed1)
        first,_ = optimize(model(),how,init=init)
        every += first
     
        rseed(seed1)
        _,last = optimize(model(),how,init=init)
        every += last
        lasts[name] += last
        pops += pop1
      best = bdoms(model(), every,1)
      log = Log(every, value=decs)
      print("")
      baseline = Num()
      for one in pop0:
        _,d = log.space.closest(one,best)
      baseline + d
    for how in hows:
      name = how.__name__
      this = Num()
      for one in pop[name]:
        _,d = log.space.closest(one,best)
        this + d
      print([100 - int(100*(a - z)/(a+0.0001)) for  z,a in
            zip(this.also().range[1:4],
                baseline.also().range[1:4])],
            name)

igd()
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


