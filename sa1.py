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
ee     = math.e
pi     = math.pi

def r3(x)    : return round(x,3)
def r3s(lst) : return map(r3,lst)
def r4(x)    : return round(x,4)
def r4s(lst) : return map(r4,lst)
def r5(x)    : return round(x,5)
def r5s(lst) : return map(r5,lst)

def say(x): 
  sys.stdout.write(str(x)); sys.stdout.flush()


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
    def decide(i,retries=100):
      assert retries>0,'cannot satisfy constraints while creating'
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
    def bdom(i,x,y,_=None):
        betters = False
        for u,v,meta in zip(x.objs,y.objs,i.objs):
            if meta.better(u,v):
                betters =True
            elif u != v:
                return False
        return betters
    def cdom(i,x, y,space):
      def w(better):
        return -1 if better == lt else 1
      def expLoss(better,x,y,n):
        return -1*ee**( w(better)*(x - y) / n )
      def loss(s,x, y):
        x,y    = x.objs, y.objs
        x      = [space.norm(x1,m) for m,x1 in enumerate(x)]
        y      = [space.norm(y1,m) for m,y1 in enumerate(y)]
        n      = min(len(x), len(y)) #lengths should be equal
        losses = [ expLoss(meta.better,xi,yi,n)
                   for xi, yi,meta
                   in zip(x,y,i.objs) ]
        return sum(losses) / n
      return x if loss("x<y",x,y) < loss("y>x",y,x) else y
 

      
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

class DTLZ7(Model):
  def __init__(i,dec=10,obj=2):
    i.dec, i.obj= 10,2
  def about(i):
    def f(x):
      if x < i.dec - 1: return x
    def g(x):
      return 1 + 9/(i.obj)*sum(x for x in x.decs)
    def h(lst,m):
      return len(lst) -1 - sum(fg(f) for f in lst)

class DTLZ7(model):
  def __init__(i,nobjs=2):
    i.ndecs, i.nobjs = nobjs-1,nobjs
  def g(i,x):
    g= 1 + 9/i.nobjs * sum(x.decs)
  def h(i,x,g):
    _h = i.nobjs
    for j in range(x.nobjs-1):
      _h -= i.f(x,j) /(1 + g) * (
              1 + math.sin(3 * pi * i.f(x,j)))
    return _h
  def f(i,j,x):
    if j < i.nobjs - 1:
      return i.decs[j]
    else:
      _g = i.g(x)
      return (1+ _g) * i.h(x,_g)

    #XXX complete dtlz7
    
class Fonseca(Model):
  n=3
  def about(i):
    def f1(can):
      z = sum([(x - 1/sqrt(Fonseca.n))**2 for x in can.decs])
      return 1 - ee**(-1*z)
    def f2(can):
      z = sum([(x + 1/sqrt(Fonseca.n))**2 for x in can.decs])
      return 1 - ee**(-1*z)
    def dec(x):
      return An(x, lo=-4, hi=4)
    i.decs = [dec(x) for x in range(Fonseca.n)]
    i.objs = [Less("f1",  maker=f1),
              Less("f2",  maker=f2)]    

class Viennet4(Model):
  n=2
  def ok(i,can):
     one,two = can.decs
     g1 = -1*two - 4*one + 4
     g2 = one + 1            
     g3 = two - one + 2
     return g1 >= 0 and g2 >= 0 and g3 >= 0
  def about(i):
    def f1(can):
      one,two = can.decs
      return (one - 2)**2 /2 + (two + 1)**2 /13 + 3
    def f2(can):
      one,two = can.decs
      return (one + two - 3)**2 /175 + (2*two - one)**2 /17 - 13
    def f3(can):
      one,two= can.decs
      return (3*one - 2*two + 4)**2 /8 + (one - two + 1)**2 /27 + 15
    def dec(x):
      return An(x,lo= -4,hi= 4)
    i.decs = [dec(x) for x in range(Viennet4.n)]
    i.objs = [Less("f1",maker=f1),
              Less("f2",maker=f2),
              Less("f3",maker=f3)]   
    
# meed hi los on decsions and objectives

class Space:
  def __init__(i,one,value=same):
    i.value = value
    i.cache = {}
    lst     = value(one)
    i.lo    = [0 for _ in lst]
    i.hi    = [0 for _ in lst]
    i.update(one)
  def updates(i,lst=[]):
    map(i.update,lst)
  def update(i,one):
    for n,(lo,hi,new) in enumerate(zip(i.lo, i.hi,
                                       i.value(one))):
      if new > hi:
        i.hi[n] = new
      if new < lo:
        i.lo[n] = new
      
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
    if x < i.lo[n]: i.lo[n] = x
    if x > i.hi[n]: i.hi[n] = x
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
      if x**2 > a**2:
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

def graph_it3(population, name, scale):
    directory = 'models/'
    file_name = directory + name
    f1 = np.array([one.x for one in population])
    f2 = np.array([one.y for one in population])
    f3 = np.array([one.z for one in population])
    fig = plt.figure()
    ax = fig.add_subplot(111) #,projection="3d")
    ax.scatter(f1, f2,f3, s = 40, color = '#000080', alpha=0.80)
    ax.set_xlim(scale[0])
    ax.set_ylim(scale[1])
    
    ax.set_zlim(scale[2])
    ax.set_xlabel('f1')
    ax.set_ylabel('f2')
    ax.set_zlabel('f3')
    fig.savefig(file_name)

def graph_it2(population, name, scale):
    directory = 'models/'
    file_name = directory + name
    f1 = np.array([one.x for one in population])
    f2 = np.array([one.y for one in population])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(f1, f2, s = 40, color = '#000080', alpha=0.80)
    #ax.set_xlim(scale[0])
    #ax.set_ylim(scale[1])
    
    ax.set_xlabel('f1')
    ax.set_ylabel('f2')
    fig.savefig(file_name)
    

def mutate(one,log=None,p=0.33, value=same,evaluate=None,ok=None,retries=100):
  tmp= o(objs=None,
         decs = [mutate1(old,p,log.space.lo[n],log.space.hi[n])
                   for n,old
                   in enumerate(value(one))])
  if ok:
    assert retries > 0,'too hard to satisfy constraints in mutation'
    if not ok(tmp):
      return mutate(one,
                    log=log,p=p, value=value,
                    evaluate=evaluate, ok=ok,
                    retries=retries - 1)
  return evaluate(tmp) if evaluate else tmp

def mutate1(old,p,lo,hi):
  x = (hi - lo)
  y = old if p >= r() else lo + x*r()
  return bound(y,lo,hi)

def bound(x, lo, hi):
  return lo + ((x - lo) % (hi - lo))

def decs(x): return x.decs
def objs(x): return x.objs
    
def normmean(log,lst):
  lst = [log.space.norm(x,n) for n,x in enumerate(lst)]
  return sum(lst)/ len(lst)

def saControl(kmax,era,cooling,verbose=False):
  def newEra():
    return not now in reports
  def startNewEra(sb,eb):
    reports[now] = o(lt=0,stagger=0,eb=eb,sb=sb, better=0, e=[])
  def oldEra():
    return (now - 1) in reports
  def finishOldEra():
    old = reports[now-1]
    sb  = old.sb
    eb  = old.eb
    if verbose:
      print("%4d::" %k,r4(old.eb)," ",
          o(lt=old.lt,stagger=old.stagger,better=old.better),
          end="")
      print(("  * %s" % sb.objs) if old.better > 0 else "")
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

def doNothing(model,pop,*l,**d):
  return pop
  
def optimize(model,how,seed=1,init=10,verbose=False,retries=100,**d):
  rseed(seed)
  pop0   = [model.eval(model.decide(retries=retries))
             for one in xrange(init)]
  #check1(">",pop0)
  logDecs = Log(pop0, value=decs)
  logObjs = Log(pop0, value=objs)
  pop = how(model,pop0[:],logDecs,logObjs, verbose=verbose,**d)
  #check1("<",pop)
  return pop0,pop

def check(s,(a,z)):
  return 1
  print("")
  a = sorted(a[:],key=objs)
  z = sorted(z[:],key=objs)
  l = len(a)
  mid = l // 2
  for i in range(0,5) + [-1] + range(mid-2,mid+2) + [-1] + range(l - 5, l -1):
    if i == -1:
      print("")
    else:
      print(s,i,"b4",a[i].objs,"now",z[i].objs)

def check1(s,a):
  return 1
  a = sorted(a[:],key=objs)
  l = len(a)
  mid = l // 2
  for i in range(0,5) + [-1] + range(mid-2,mid+2) + [-1] + range(l - 5, l -1):
    if i == -1:
      print("")
    else:
      print(i,s,a[i].objs)

  
def threeD(threes,name,value=same):
  all = [(o(),value(one)[:3]) for one in threes]
  for a,x in all:
    a.x = x[0]
    a.y = x[1]
    a.z = x[2]
  graph_it3( [x[0] for x in all],name,(1,1,1))

def twoD(twos,name,value=same):
  all = [(o(),value(one)[:2]) for one in twos]
  for a,x in all:
    a.x = x[0]
    a.y = x[1]
  graph_it2( [x[0] for x in all],name,(1,1))
  
def sa(model,_,
       logDecs,logObjs,
       era=50,
       kmax=1000, 
       aggr=normmean,
       cooling=2,
       retries=100,
       p=0.33,
       verbose=False,
       **d):
  print(verbose)
  sb = s = model.decide()
  eb = e = aggr(logObjs,model.eval(s).objs)
  for t,now,history in saControl(kmax,era,cooling,verbose):
    sn  = mutate(s, p        = p,
                    ok       = model.ok,
                    log      = logDecs,
                    value    = decs,
                    retries  = retries,
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

def dump(all,f,mode="w"):
  where = open(f,mode)
  where.write("####\n")
  for one in all:
    print(one)
    where.write(", ".join(map(str,one)))
    where.write("\n")
  where.close()
  
def de(model,frontier,logDecs,logObjs,era=50,repeats=10,verbose=False,cr=0.3,f=0.75):
  zero = frontier[:]
  for r in xrange(repeats):
    for n,parent in enumerate(frontier):
      child = smear(frontier,log=logDecs,f=f,
                    cr=cr,evaluate=model.eval)
      logDecs + child
      logObjs + child
      if model.bdom(child,parent,logObjs.space):
          frontier[n] = child
    check(r,(zero,frontier))
  return frontier

def bdoms(model,frontier,*_,**d):
  for x in frontier:
    x.alive = True
  for x in frontier:
    for y in frontier:
      if model.bdom(x,y):
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

# freeze distance to be min max on whole space
def igd(models=[Fonseca,ZDT1],hows=[sa,de,bdoms],
        repeats=5, seed0=1,init=300):
  class metas:
    def __init__(i,how):
      i.how  = how
      i.name = how.__name__
      i.last  = {}
      i.first = {}
  hows = [metas(how) for how in hows]
  for model in models:
    print(model.__name__)
    rseed(seed0)
    every = []
    firsts = []
    lasts = []
    bests = []
    for n in xrange(repeats):
      say("|")
      seed1 = r()
      for meta in hows:
        say(".")
        a,z = optimize(model(),how,seed=seed1,
                       init=init,repeats=repeats)
        meta.last[seed1]  = z
        meta.first[seed1] = a
        firsts += a
        lasts += z
        every += a
        every += z
        bests = bdoms(model(),bests+z ,1)
    say("!")
    print("")
    print(len(every))
    space = Space(every[0],value=objs)
    space.updates(every)
    say("\n")
    for meta in hows:
       baseline = Num()
       better   = Num()
       for k in meta.last:
         for a in bdoms(model(),meta.first[k]):
           _,d = space.closest(a,bests)
           baseline + d
         for z in meta.last[k]:
           _,d = space.closest(z,bests)
           better + d
       print("\n",meta.name)
       print(baseline.also().range)
       print(better  .also().range)
       
def ranges(space,best,what):
  return Num([space.closest(one,best)[1] for one in what]).also().range[1:4]

def better(a,z):
  return a/(z + 0.000000001)
#return 100 - int(100*abs((a - z))/(a + 0.000001)) #/(a+0.0001) #int(100*(1 - ((a - z)/(a+0.00001))))
       
#igd()
#print(10*len(Fonseca().decs))
#optimize(ZDT1(),de,init=300,repeats=1,verbose=True)
igd(models=[ZDT1,Fonseca],hows=[de])
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


