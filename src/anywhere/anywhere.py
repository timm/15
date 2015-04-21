from __future__ import print_function,division
import random, pprint, re, pprint

isa   = isinstance
fun   = lambda x:x.__class__.__name__ == 'function'
r     = random.random
any   = random.choice
rseed = random.seed

def shuffle(lst):
  random.shuffle(lst)
  return lst

def show(x,indent=2,width=60):
  pprint.pformat(x,indent=indent,width=width)
  
#------------------------------------------------
def ok(*lst):
  for one in lst: unittest(one)
  return one
  
class unittest:
  tries = fails = 0  #  tracks the record so far
  def __init__(i,test):
    unittest.tries += 1
    try:
      test()
    except Exception,e:
      unittest.fails += 1
      i.report(e,test)
  def report(i,e,test):
    print("# TRIES= %s FAIL= %s TEST= %s : %s"  % (
          unittest.tries, unittest.fails,
          test.__name__, e))

#------------------------------------------------
class o:
  def __init__(i,**d)    : i.add(**d)
  def d(i)               : return i.__dict__
  def add(i,**d)         : i.d().update(d);return i
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __getitem__(i,k)   : return i.__dict__[k] 
  def __repr__(i)        : return show(has(i))
  
def has(x,  decimals=5, wicked=False) :
  if   isa(x, o):
    return has({'o': x.d()})
  elif isa(x,list):
    return map(has,x)
  elif isa(x,float):
    return round(x,decimals)
  elif fun(x):
    return x.__name__+'()'
  elif wicked and hasattr(x,"__dict__"):
    return has({x.__class__.__name__ : x.__dict__})
  elif isa(x, dict):
    return {k:has(v) for k,v in x.items()}
  else:
    return x
     
#------------------------------------------------
def readcsv(file, t = None): 
  for cells in lines(file):
    if t:
      row(t,cells)
    else:
      t = table(cells)
  return t

def lines(file, bad  = r'(["\' \t\r\n]|#.*)',
                sep  = "" ) :
  def atom(x):
    try : return int(x)
    except ValueError:
      try : return float(x)
      except ValueError : return x
  kept = ""
  for line in open(file):
    now   = re.sub(bad,"",line)
    kept += now
    if kept:
      if not now[-1] == sep:
        yield map(atom, kept.split(sep))
        kept = ""
        
#------------------------------------------------    
def row(t,cells, skip='?'):
  t += [cells]
  for i,cell in enumerate(cells):
    if cell != skip:
      if i in t.num:
        hdr    = t.num[i]
        hdr.lo = min(cell, hdr.lo)
        hdr.hi = max(cell, hdr.hi)

def table(cells, num  = '$', less = '<',
                 more = '>', skip = "?" ):
  t = o(name={}, num={},  sym={},  rows=[],
        less={}, more={}, goal={},
        fields=cells )
  def nump(cell):
    for char in [num, less, more]:
      if char in cell:
         return True
  for i,cell in enumerate(cells):
    t.name[i] = cell
    if nump(cell):
      t.num[i] = o(hi = -1*10**32, lo = 10**32)
    else:
      t.sym[i] = i
    if less in cell:
      t.goal[i] = t.less[i] = i
    if more in cell:
      t.goal[i] = t.more[i] = i
    if not i in t.goal:
      t.indep[i] = i
  return t

def clone(t) { return table(t.fields) }
                    
#------------------------------------------------    
def norm(i,r):
  return (i - r.lo) / (r.hi - r.lo + 0.00001)

def trim(n,r):
  return max(r.lo, min(n, r.hi))

def dist(cells1,cells2,t, skip="?"):
  n = inc = 0
  for col in t.indep:
    x = cells1[col]
    y = cells2[col]
    if x==skip and y==skip:
      continue
    n += 1
    if col in t.sym:
      inc  += 0 if x==y else 1
    else:
      if x != skip: x= norm(x,t.num[col])
      if y != skip: y= norm(y,t.num[col])
      if x == skip: x= 1 if y<0.5 else 0
      if y == skip: y= 1 if x<0.5 else 0
      inc  += (x-y)**2
  return inc**0.5 / n**0.5

#------------------------------------------------    

